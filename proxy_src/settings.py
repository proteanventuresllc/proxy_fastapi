from typing import List, Union

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    target_host: str
    retry_codes: Union[str, List[int]] = Field(..., env="RETRY_CODES")

    @validator('retry_codes', pre=True)
    def retry_list(cls, codes):
        if isinstance(codes, str):
            return [int(item.strip()) for item in codes.split(",")]
        return [int(codes)]

settings = Settings()
