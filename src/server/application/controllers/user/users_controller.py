# -*- coding: utf-8 -*-


from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.core.application.dtos.common.base_request import IdListDto
from src.core.application.dtos.common.base_response import SuccessResponse
from src.core.application.dtos.user.users_dto import (
    CoreCreateUsersDto,
    CoreUpdateUsersDto,
    CoreUsersDto,
)
from src.server.application.use_cases.user.users_use_case import UsersUseCase
from src.server.infrastructure.di.server_container import ServerContainer

router = APIRouter()


@router.post(
    "/user",
    summary="유저 생성",
    response_model=SuccessResponse[CoreUsersDto],
    response_model_exclude={"pagination"},
)
@inject
async def create_user(
    create_data: CoreCreateUsersDto,
    user_use_case: UsersUseCase = Depends(
        Provide[ServerContainer.user_container.users_use_case]
    ),
) -> SuccessResponse[CoreUsersDto]:
    data = await user_use_case.create_data(create_data=create_data)
    return SuccessResponse(data=data)


# ==========================================================================================


@router.post(
    "/users",
    summary="유저 생성 (복수)",
    response_model=SuccessResponse[List[CoreUsersDto]],
    response_model_exclude={"pagination"},
)
@inject
async def create_users(
    create_datas: List[CoreCreateUsersDto],
    user_use_case: UsersUseCase = Depends(
        Provide[ServerContainer.user_container.users_use_case]
    ),
) -> SuccessResponse[List[CoreUsersDto]]:
    data = await user_use_case.create_datas(create_datas=create_datas)
    return SuccessResponse(data=data)


# ==========================================================================================


@router.get(
    "/users",
    summary="유저 정보 모두 조회",
    response_model=SuccessResponse[List[CoreUsersDto]],
)
@inject
async def get_users(
    page: int = 1,
    page_size: int = 10,
    user_use_case: UsersUseCase = Depends(
        Provide[ServerContainer.user_container.users_use_case]
    ),
) -> SuccessResponse[List[CoreUsersDto]]:
    data, pagination = await user_use_case.get_datas(page=page, page_size=page_size)
    return SuccessResponse(data=data, pagination=pagination)


# ==========================================================================================


@router.get(
    "/user/{user_id}",
    summary="유저 정보 조회",
    response_model=SuccessResponse[CoreUsersDto],
    response_model_exclude_none=True,
    response_model_exclude={"pagination"},
)
@inject
async def get_user_by_user_id(
    user_id: int,
    user_use_case: UsersUseCase = Depends(
        Provide[ServerContainer.user_container.users_use_case]
    ),
) -> SuccessResponse[CoreUsersDto]:
    data = await user_use_case.get_data_by_data_id(data_id=user_id)
    return SuccessResponse(data=data)


# ==========================================================================================


@router.post(
    "/users/by-ids",
    summary="ID 리스트로 유저 여러 명 조회",
    response_model=SuccessResponse[List[CoreUsersDto]],
    response_model_exclude={"pagination"},
)
@inject
async def get_users_by_ids(
    payload: IdListDto,
    user_use_case: UsersUseCase = Depends(
        Provide[ServerContainer.user_container.users_use_case]
    ),
) -> SuccessResponse[List[CoreUsersDto]]:
    data = await user_use_case.get_datas_by_data_ids(payload=payload)
    return SuccessResponse(data=data)


# ==========================================================================================


@router.put(
    "/user/{user_id}",
    summary="유저 수정",
    response_model=SuccessResponse[CoreUsersDto],
    response_model_exclude={"pagination"},
)
@inject
async def update_user_by_user_id(
    user_id: int,
    update_data: CoreUpdateUsersDto,
    user_use_case: UsersUseCase = Depends(
        Provide[ServerContainer.user_container.users_use_case]
    ),
) -> SuccessResponse[CoreUsersDto]:
    data = await user_use_case.update_data_by_data_id(
        data_id=user_id, update_data=update_data
    )
    return SuccessResponse(data=data)


# ==========================================================================================


@router.delete(
    "/user/{user_id}",
    summary="유저 삭제",
    response_model=SuccessResponse,
    response_model_exclude={"data", "pagination"},
)
@inject
async def delete_user_by_user_id(
    user_id: int,
    users_use_case: UsersUseCase = Depends(
        Provide[ServerContainer.user_container.users_use_case]
    ),
) -> SuccessResponse:
    success = await users_use_case.delete_data_by_data_id(data_id=user_id)
    return SuccessResponse(success=success)
