from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.YandexSpeller.main import check_text
from src.auth.base_config import current_active_user
from src.auth.models import User
from src.database import get_async_session
from src.notes.models import Notes

from src.notes.schemas import Note

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


@router.get("/", response_model=List[Note], status_code=status.HTTP_200_OK)
async def get_notes(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user)
):
    try:
        query = (
            select(Notes)
            .where((Notes.user_id == user.id))
        )
        result = await session.execute(query)
        result_notes = result.scalars().all()

        return result_notes

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def new_notes(
        note: str,
        need_to_check_text: bool = False,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user)
):
    try:
        if need_to_check_text:
            check_result = await check_text(note)
            if check_result:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=check_result)

        new_note = Notes(
            user_id=user.id,
            text=note
        )
        session.add(new_note)
        await session.flush()
        new_note_id = new_note.UUID

        await session.commit()

        return {"id": new_note_id}


    except HTTPException as http_exc:
        await session.rollback()
        raise http_exc

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_note(
        note_ids: List[UUID],
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user)
):
    try:
        if not note_ids:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Необходимо передать хотя бы один ID заметки для удаления.")

        query = (
            select(Notes)
            .where((Notes.user_id == user.id) & (Notes.UUID.in_(note_ids)))
        )
        result = await session.execute(query)
        notes_to_delete = result.scalars().all()

        if not notes_to_delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Заметки с указанным ID не найдены или принадлежат другому пользователю.")


        for note in notes_to_delete:
            await session.delete(note)

        await session.commit()
        return {"status": "success", "message": f"Заметки с ID {', '.join(str(id) for id in note_ids)} успешно удалены"}

    except HTTPException as http_exc:
        await session.rollback()
        raise http_exc

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")