def calculate_tarot_number(year: int, month: int, day: int) -> int:
    """
    생년월일을 입력받아 0~21 사이의 타로 카드 번호를 반환하는 함수
    (Soul Card 알고리즘 적용)
    """
    # 1단계: 년+월+일 합산
    # 예: 1995년 10월 24일 -> 1995 + 10 + 24 = 2029
    total_sum = year + month + day

    # 2단계: 21 이하가 될 때까지 자릿수 더하기 반복
    while total_sum > 21:
        # 예외 처리: 합이 22가 되면 0번(The Fool)으로 반환
        if total_sum == 22:
            return 0
        
        # 숫자를 문자열로 바꿔서 각 자릿수를 더함
        # 예: 2029 -> 2 + 0 + 2 + 9 = 13
        total_sum = sum(int(digit) for digit in str(total_sum))

    return total_sum

# --- 테스트 코드 ---
if __name__ == "__main__":
    # 예시 1: 스티브 잡스 (1955-02-24) -> 1955+2+24 = 1981 -> 1+9+8+1 = 19 (태양)
    print(f"스티브 잡스: {calculate_tarot_number(1955, 2, 24)}") 
    
    # 예시 2: 아이유 (1993-05-16) -> 1993+5+16 = 2014 -> 2+0+1+4 = 7 (전차)
    print(f"아이유: {calculate_tarot_number(1993, 5, 16)}")