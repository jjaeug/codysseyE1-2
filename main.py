
import json
import os


DATA_FILE = "quiz_data.json"


class Quiz:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def check_answer(self, user_answer):
        return user_answer.strip().lower() == self.answer.strip().lower()


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.score = 0
        self.load_data()

    def create_default_data(self):
        default_data = {
            "score": 0,
            "quizzes": [
                {"question": "파이썬에서 출력할 때 사용하는 함수는?", "answer": "print"},
                {"question": "리스트를 만들 때 사용하는 괄호는? 예: [1, 2, 3]", "answer": "[]"},
                {"question": "문자열을 나타낼 때 사용하는 기호는? 예: 'hello'", "answer": "'"},
                {"question": "조건문에 사용하는 키워드는?", "answer": "if"},
                {"question": "반복문 중 하나로, 정해진 범위를 반복할 때 쓰는 키워드는?", "answer": "for"}
            ]
        }

        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(default_data, file, ensure_ascii=False, indent=4)

    def load_data(self):
        try:
            if not os.path.exists(DATA_FILE):
                self.create_default_data()

            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.score = data["score"]
            self.quizzes = [
                Quiz(item["question"], item["answer"])
                for item in data["quizzes"]
            ]

        except FileNotFoundError:
            print("데이터 파일을 찾을 수 없어 새로 생성합니다.")
            self.create_default_data()
            self.load_data()

        except json.JSONDecodeError:
            print("JSON 파일 형식이 잘못되었습니다. 데이터를 초기화합니다.")
            self.create_default_data()
            self.load_data()

        except KeyError:
            print("JSON 데이터에 필요한 키가 없습니다. 데이터를 초기화합니다.")
            self.create_default_data()
            self.load_data()

        except PermissionError:
            print("파일 접근 권한이 없습니다.")

        except Exception as error:
            print("알 수 없는 오류가 발생했습니다:", error)

    def save_data(self):
        try:
            data = {
                "score": self.score,
                "quizzes": [
                    {
                        "question": quiz.question,
                        "answer": quiz.answer
                    }
                    for quiz in self.quizzes
                ]
            }

            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        except PermissionError:
            print("파일 저장 권한이 없습니다.")

        except OSError:
            print("파일 저장 중 시스템 오류가 발생했습니다.")

    def play_quiz(self):
        if len(self.quizzes) == 0:
            print("등록된 퀴즈가 없습니다.")
            return

        print("\n=== 퀴즈 풀기 ===")

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n문제 {index}. {quiz.question}")
            user_answer = input("정답 입력: ")

            if quiz.check_answer(user_answer):
                print("정답입니다!")
                self.score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer} 입니다.")

        self.save_data()
        print(f"\n현재 점수: {self.score}")

    def show_score(self):
        print(f"\n현재 누적 점수는 {self.score}점입니다.")
    def add_quiz(self):
        print("\n=== 퀴즈 추가 ===")

        question = input("문제를 입력하세요: ").strip()
        answer = input("정답을 입력하세요: ").strip()

        if question == "" or answer == "":
            print("문제와 정답은 비워둘 수 없습니다.")
            return

        new_quiz = Quiz(question, answer)
        self.quizzes.append(new_quiz)
        self.save_data()

        print("새 퀴즈가 추가되었습니다.")
    def reset_score(self):
        print("\n=== 점수 초기화 ===")

        confirm = input("정말 점수를 초기화하시겠습니까? (y/n): ").strip().lower()

        if confirm == "y":
            self.score = 0
            self.save_data()
            print("점수가 0점으로 초기화되었습니다.")
        else:
            print("점수 초기화를 취소했습니다.")
    def show_quizzes(self):
        print("\n=== 퀴즈 목록 ===")

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")
            print(f"   정답: {quiz.answer}")
    def show_menu(self):
        while True:
            print("\n=== 콘솔 퀴즈 게임 ===")
            print("1. 퀴즈 풀기")
            print("2. 점수 보기")
            print("3. 퀴즈 추가")
            print("4. 점수 초기화")
            print("5. 퀴즈 목록 보기")
            print("6. 종료")

            choice = input("메뉴를 선택하세요: ")

            if choice == "1":
                self.play_quiz()
            elif choice == "2":
                self.show_score()
            elif choice == "3":
                self.add_quiz()
            elif choice == "4":
                self.reset_score()
            elif choice == "5":
                self.show_quizzes()
            elif choice == "6":
                print("게임을 종료합니다.")
                break
            else:
                print("1, 2, 3, 4, 5, 6 중에서 선택하세요.")


def main():
    game = QuizGame()
    game.show_menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n게임을 종료합니다.")
    except EOFError:
        print("\n입력이 종료되었습니다.")