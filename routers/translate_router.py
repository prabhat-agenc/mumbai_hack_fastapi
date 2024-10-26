from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from google.cloud import translate_v2 as translate
from typing import Optional, List
from dotenv import load_dotenv
import httpx
import os

load_dotenv()
router = APIRouter()

API_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
BASE_URL = "https://translation.googleapis.com/language/translate/v2"


class BatchTranslationRequest(BaseModel):
    texts: List[str]
    target_language: str

class BatchTranslationResponse(BaseModel):
    translations: List[str]
    target_language: str

class Language(BaseModel):
    code: str
    name: str

@router.post("/translate/batch", response_model=BatchTranslationResponse)
async def translate_text(request: BatchTranslationRequest):
    try:
        # Prepare the request parameters
        params = {
            "key": API_KEY,
            "target": request.target_language,
            "q": request.texts
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(BASE_URL, params=params)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Translation API Error: {response.text}",
            )

        result = response.json()

        if "data" not in result or "translations" not in result["data"]:
            raise HTTPException(
                status_code=500,
                detail="Unexpected response format from Translation API",
            )
        
        translations = [
            translation["translatedText"] 
            for translation in result["data"]["translations"]
        ]

        return BatchTranslationResponse(
            translations=translations,
            target_language=request.target_language
        )

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/languages", response_model=List[Language])
async def get_languages():
    try:
        params = {"key": API_KEY, "target": "en"}  # Get language names in English

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/languages", params=params)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail=f"API Error: {response.text}"
            )

        data = response.json()
        languages = []
        for lang in data["data"]["languages"]:
            languages.append(Language(code=lang["language"], name=lang["name"]))

        # Sort languages by name for easier reading
        languages.sort(key=lambda x: x.name)
        return languages

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/supported-languages")
async def get_supported_languages():
    try:
        params = {
            "key": API_KEY,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/languages", params=params)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail=f"API Error: {response.text}"
            )

        return response.json()

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
