import csv
from bard.models import Test, Question, Answer  # Замените 'your_app' на название вашего Django-приложения


def import_data(csv_filename):
    with open(csv_filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for row in reader:
            test_title, question_text, *answers, correct_answer = row['Test Title'], row['Question'], row['Answer 1'], \
            row['Answer 2'], row['Answer 3'], row['Correct Answer']

            test, _ = Test.objects.get_or_create(title=test_title)
            question = Question.objects.create(text=question_text, test=test)

            for i in range(1, 4):  # Предполагаем, что у нас есть 3 ответа
                is_correct = (str(i) == correct_answer.strip())
                Answer.objects.create(
                    question=question,
                    text=row[f'Answer {i}'],
                    is_correct=is_correct
                )


# Вызовите функцию с путем к файлу CSV
import_data('path/to/your/file.csv')  # Замените на актуальный путь к файлу
