import os
from dotenv import load_dotenv
from openai import OpenAI
from tarot_data import tarot_card_data
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY가 설정되지 않았습니다. (.env 확인)")

client = OpenAI(api_key=api_key)

MAX_CHARS = 12000  # 초보 단계에서는 길이 초과를 막기 위해 상한

def build_prompt(lunar_card_data, solar_card_data) -> str:
    lunar_str = json.dumps(lunar_card_data, ensure_ascii=False, indent=2)
    solar_str = json.dumps(solar_card_data, ensure_ascii=False, indent=2)
    return f"""
음력 탄생카드는 내재적 자아로 타고한 성향, 양력 탄생카드는 외재적 자아로 발현되기 쉬운 성향를 상징하니 각각의 해석과 상호작용에 대해서 해석해주세요. 상담 결과는 한 문단으로 가독성 있게 출력하고 상담자가 콘텐츠 기획자로서 연구하기에 좋은 유행성과 관련성을 갖춘 키워드를 추천하세요.

음력 탄생카드 정보: {lunar_str}
양력 탄생카드 정보: {solar_str}
[출력 형식]
# 해석 요약

## 키워드 (5개, 쉼표로)
키워드1, 키워드2, 키워드3, 키워드4, 키워드5

""".strip()

def summarize_txt(lunar_card, solar_card) -> str:
    lunar_data=tarot_card_data["cards"][lunar_card]
    solar_data=tarot_card_data["cards"][solar_card]
    user_prompt = build_prompt(lunar_data, solar_data)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[{"role": "user", "content": user_prompt},
                  {"role": "system", "content": "당신은 20년 경력의 전문 타로 상담사입니다. 내담자의 마음을 공감해주고, 신비롭지만 희망적인 어조로 말해야 합니다."}],
    )
    return resp.choices[0].message.content

def main() -> None:
    print("예제")
    solar_card_number = 4  # 예: 황제 (Emperor)
    lunar_card_number = 9  # 예: 은둔자 (Hermit)
    print(f"양력카드:{solar_card_number} (황제)")
    print(f"음력카드:{lunar_card_number} (은둔자)")
    summary = summarize_txt(solar_card_number, lunar_card_number)
    print(f"해석 요약:{summary}")


if __name__ == "__main__":
    main()
