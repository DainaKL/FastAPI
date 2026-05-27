from typing import Optional
from fastapi import APIRouter, Depends, status, Form, File, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.dependencies.auth import get_current_user
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository
from src.infrastructure.sqlite.repositories.comment_image_repository import CommentImageRepository
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.schemas.comments import Comment, CommentUpdate
from src.schemas.users import User as UserSchema
from src.services.media_uploader import save_file
from src.domain.comment.use_cases.create_comment import CreateCommentUseCase
from src.domain.comment.use_cases.delete_comment import DeleteCommentUseCase
from src.domain.comment.use_cases.get_comments import GetCommentsUseCase
from src.domain.comment.use_cases.get_comment import GetCommentUseCase
from src.domain.comment.use_cases.update_comment import UpdateCommentUseCase
from src.core.exceptions.api_exceptions import (
    NotFoundException,
    CommentForbiddenException,
    InvalidIDException,
)
from src.core.exceptions.domain_exceptions import PostNotFoundException

router = APIRouter(prefix="/comments", tags=["Comments"])


def validate_id(id: int) -> int:
    if id <= 0:
        raise InvalidIDException(id)
    return id


@router.get("/", response_model=list[Comment])
async def get_comments(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db),
):
    repo = CommentRepository()
    use_case = GetCommentsUseCase(repo)
    comments = await use_case.execute(session, skip=skip, limit=limit)
    return comments


@router.get("/published", response_model=list[Comment])
async def get_published_comments(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db),
):
    repo = CommentRepository()
    comments = await repo.get_published(session, skip=skip, limit=limit)
    return [Comment.model_validate(c) for c in comments]


@router.get("/{comment_id}", response_model=Comment)
async def get_comment(
    comment_id: int,
    session: AsyncSession = Depends(get_db),
):
    validate_id(comment_id)
    repo = CommentRepository()
    use_case = GetCommentUseCase(repo)
    comment = await use_case.execute(session, comment_id)
    return comment


@router.get("/post/{post_id}", response_model=list[Comment])
async def get_comments_by_post(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db),
):
    validate_id(post_id)
    repo = CommentRepository()
    comments = await repo.get_by_post(session, post_id, skip=skip, limit=limit)
    return [Comment.model_validate(c) for c in comments]


@router.get("/author/{author_id}", response_model=list[Comment])
async def get_comments_by_author(
    author_id: int,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db),
):
    validate_id(author_id)
    repo = CommentRepository()
    comments = await repo.get_by_author(session, author_id, skip=skip, limit=limit)
    return [Comment.model_validate(c) for c in comments]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Comment)
async def create_comment(
    text: str = Form(...),
    post_id: int = Form(...),
    is_published: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    session: AsyncSession = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
):
    repo = CommentRepository()
    post_repo = PostRepository()
    user_repo = UserRepository()
    
    try:
        use_case = CreateCommentUseCase(repo, post_repo, user_repo)
        comment_data = {"text": text, "post_id": post_id, "author_id": current_user.id, "is_published": is_published}
        new_comment = await use_case.execute(session, comment_data)

        if image:
            url = await save_file(image)
            img_repo = CommentImageRepository()
            await img_repo.add(session, new_comment.id, url)
            await session.flush()
            new_comment = await repo.get_by_id(session, new_comment.id)

        await session.commit()
        return Comment.model_validate(new_comment)
    except PostNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFoundByIdException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{comment_id}", response_model=Comment)
async def update_comment(
    comment_id: int,
    text: Optional[str] = Form(None),
    is_published: Optional[bool] = Form(None),
    session: AsyncSession = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
):
    validate_id(comment_id)
    repo = CommentRepository()
    comment = await repo.get_by_id(session, comment_id)
    if not comment:
        raise NotFoundException(detail=f"Comment {comment_id} not found")
    if not current_user.is_admin and comment.author_id != current_user.id:
        raise CommentForbiddenException(action="редактировать")
    
    use_case = UpdateCommentUseCase(repo)
    update_data = {}
    if text is not None:
        update_data["text"] = text
    if is_published is not None:
        update_data["is_published"] = is_published
    
    if update_data:
        updated = await use_case.execute(session, comment_id, update_data)
        await session.commit()
        return Comment.model_validate(updated)
    
    return Comment.model_validate(comment)


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
):
    validate_id(comment_id)
    repo = CommentRepository()
    comment = await repo.get_by_id(session, comment_id)
    if not comment:
        raise NotFoundException(detail=f"Comment {comment_id} not found")
    if not current_user.is_admin and comment.author_id != current_user.id:
        raise CommentForbiddenException(action="удалять")
    
    use_case = DeleteCommentUseCase(repo)
    await use_case.execute(session, comment_id)
    await session.commit()
    return {"status": "success", "message": f"Comment {comment_id} deleted"}


@router.post("/{comment_id}/images/")
async def add_comment_image(
    comment_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
):
    repo = CommentRepository()
    comment = await repo.get_by_id(session, comment_id)
    if not comment:
        raise NotFoundException(detail=f"Comment {comment_id} not found")
    if comment.author_id != current_user.id:
        raise CommentForbiddenException(action="добавлять изображения к чужому комментарию")
    
    url = await save_file(file)
    img_repo = CommentImageRepository()
    await img_repo.add(session, comment_id, url)
    await session.commit()
    return {"message": "Image added", "url": url}
