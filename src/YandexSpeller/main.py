import aiohttp

async def check_text(text):

    url = "https://speller.yandex.net/services/spellservice.json/checkText"

    params = {
        'text': text,
        'lang': 'ru,en',
        'options': 0
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                return {"status": "error", "message": f"Ошибка при обращении к API Yandex Speller: {response.status}"}
            results = await response.json()
            if results:
                errors_list = [
                    {"word": error["word"],
                     "suggestions": error["s"]}
                    for error in results
                ]
                return {"status": "errors_found", "errors": errors_list}
            else:
                return None