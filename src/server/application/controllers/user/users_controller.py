# -*- coding: utf-8 -*-


from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.core.application.dtos.base_dto import IdListDto
from src.core.application.dtos.user.users_dto import (
    CoreCreateUsersDto,
    CoreUpdateUsersDto,
    CoreUsersDto,
)
from src.core.application.responses.base_response import BaseResponse
from src.server.application.use_cases.user.users_use_case import UsersUseCase
from src.server.infrastructure.di.server_container import ServerContainer

router = APIRouter()


@router.post(
    "/user",
    summary="유저 생성",
    tags=["유저"],
    response_model=BaseResponse[CoreUsersDto],
    response_model_exclude={"pagination", "exists"},
)
@inject
async def create_user(
    create_data: CoreCreateUsersDto,
    user_use_case: UsersUseCase = Depends(
        Provide[ServerContainer.user_container.users_use_case]
    ),
) -> BaseResponse[CoreUsersDto]:
    data = await user_use_case.create_data(create_data=create_data)
    return BaseResponse(data=data)


# ==========================================================================================


@router.post(
    "/users",
    summary="유저 생성 (복수)",
    tags=["유저"],
    response_model=BaseResponse[List[CoreUsersDto]],
    response_model_exclude={"pagination", "exists"},
)
@inject
async def create_users(
    create_datas: List[CoreCreateUsersDto],
    user_use_case: UsersUseCase = Depends(
        Provide[ServerContainer.user_container.users_use_case]
    ),
) -> BaseResponse[List[CoreUsersDto]]:
    data = await user_use_case.create_datas(create_datas=create_datas)
    return BaseResponse(data=data)


# ==========================================================================================


@router.get(
    "/users",
    summary="유저 정보 모두 조회",
    tags=["유저"],
    response_model=BaseResponse[List[CoreUsersDto]],
    response_model_exclude={"exists"},
)
@inject
async def get_users(
    page: int = 1,
    page_size: int = 10,
    user_use_case: UsersUseCase = Depends(
        Provide[ServerContainer.user_container.users_use_case]
    ),
) -> BaseResponse[List[CoreUsersDto]]:
    data, pagination = await user_use_case.get_datas(page=page, page_size=page_size)
    return BaseResponse(data=data, pagination=pagination)


# ==========================================================================================


@router.get(
    "/user/{user_id}",
    summary="유저 정보 조회",
    tags=["유저"],
    response_model=BaseResponse[CoreUsersDto],
    response_model_exclude_none=True,
    response_model_exclude={"pagination", "exists"},
)
@inject
async def get_user_by_user_id(
    user_id: int,
    user_use_case: UsersUseCase = Depends(
        Provide[ServerContainer.user_container.users_use_case]
    ),
) -> BaseResponse[CoreUsersDto]:
    data = await user_use_case.get_data_by_data_id(data_id=user_id)
    return BaseResponse(data=data)


# ==========================================================================================


@router.post(
    "/users/by-ids",
    summary="ID 리스트로 유저 여러 명 조회",
    tags=["유저"],
    response_model=BaseResponse[List[CoreUsersDto]],
    response_model_exclude={"pagination", "exists"},
)
@inject
async def get_users_by_ids(
    payload: IdListDto,
    user_use_case: UsersUseCase = Depends(
        Provide[ServerContainer.user_container.users_use_case]
    ),
) -> BaseResponse[List[CoreUsersDto]]:
    data = await user_use_case.get_datas_by_data_ids(payload=payload)
    return BaseResponse(data=data)


# ==========================================================================================


@router.put(
    "/user/{user_id}",
    summary="유저 수정",
    tags=["유저"],
    response_model=BaseResponse[CoreUsersDto],
    response_model_exclude={"pagination", "exists"},
)
@inject
async def update_user_by_user_id(
    user_id: int,
    update_data: CoreUpdateUsersDto,
    user_use_case: UsersUseCase = Depends(
        Provide[ServerContainer.user_container.users_use_case]
    ),
) -> BaseResponse[CoreUsersDto]:
    data = await user_use_case.update_data_by_data_id(
        data_id=user_id, update_data=update_data
    )
    return BaseResponse(data=data)


# ==========================================================================================


@router.delete(
    "/user/{user_id}",
    summary="유저 삭제",
    tags=["유저"],
    response_model=BaseResponse,
    response_model_exclude={"data", "pagination", "exists"},
)
@inject
async def delete_user_by_user_id(
    user_id: int,
    users_use_case: UsersUseCase = Depends(
        Provide[ServerContainer.user_container.users_use_case]
    ),
) -> BaseResponse:
    success = await users_use_case.delete_data_by_data_id(data_id=user_id)
    return BaseResponse(success=success)
