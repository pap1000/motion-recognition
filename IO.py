"""2021-05-22 이범석 21:50 엑셀파일 내 플레이기록과 진행사항 저장 함수 제작"""
import openpyxl
from datetime import datetime

MAX_ROW = 8  # 총 도전과제 수 +1
MAX_COLUMN = 11  # 총 음원 수 +1

# 음원 리스트와 도전과제 리스트
SList = ['낮의 달', '스타쉽 몽상', '추적자', 'swing_swing', 'Space Town', 'New_Future', 'Funky_Junky', 'Film_Clash!',
         'Feather_of_the_Angel', 'Expantion']
Clist = ['시작이 반이다', '의지박약', '리듬천재', '단 한곡', '에어로빅 강사', '3대500', '헬창']


# 유저의 게임 진행정보를 변경(유저가 하나)
def Play_count(song):
    global date_diff, total
    for r in range(0, MAX_COLUMN - 1):
        sum = 0
        if song == SList[r]:
            wb = openpyxl.load_workbook('UserData/user.xlsx', data_only=True)
            ws = wb['Sheet']

            # 완료한 음원의 누적횟수 1회증가
            B = ws.cell(row=2, column=r + 2).value
            ws.cell(row=2, column=r + 2, value=B + 1)

            # 누적횟수를 모두 더하여 총횟수를 게산
            for r in range(2, MAX_COLUMN):
                sum += ws.cell(row=2, column=r).value

            ws.cell(row=5, column=2, value=sum)

            # 도전과제 '헬창'을 위한 날짜 계산
            last = ws.cell(row=4, column=3).value  # 최근 플레이 날짜
            today = datetime.now()  # 현재 날짜
            date_diff = today - last
            total = (today - ws.cell(row=4, column=2).value).days
            Cumul = ws.cell(row=5, column=2).value

            # 운동을 하루라도 쉰 경우
            if date_diff.days != 0 and date_diff.days != 1:
                ws.cell(row=4, column=2, value=today)
                ws.cell(row=4, column=3, value=today)

            wb.save('UserData/user.xlsx')
            wb.close()

    if date_diff.days != 0 and date_diff.days != 1:
        return 0
    else:
        return total, Cumul

# 하루 지난 플레이 기록을 삭제
def Del_record():
    wb = openpyxl.load_workbook('UserData/accuracy.xlsx', data_only=True)
    ws = wb['Sheet1']
    now = datetime.now()
    for r in range(2, ws.max_row + 1):
        compare = (now - ws.cell(row=r, column=3).value).days
        if compare != 0:
            ws.delete_rows(r)
        else:
            pass
    wb.save('UserData/accuracy.xlsx')
    wb.close()

# 플레이 정보를 기록
def Play_record(song, accuracy):
    wb = openpyxl.load_workbook('UserData/accuracy.xlsx', data_only=True)
    ws = wb['Sheet1']
    today = datetime.now()
    ws.append([song, accuracy, today])

    wb.save('UserData/accuracy.xlsx')
    wb.close()


def main(song):
    t, c = Play_count(song)
    print(c)
    if t == 100:
        print("헬창!")
    elif t == 50:
        print("에어로빅 강사")
    elif c == 1:
        print("시작이 반이다")
    else:
        pass


Del_record()
