# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
from producer.data_generator import FakeDataGenerator

if __name__ == '__main__':
    faker = FakeDataGenerator()
    for i in range(5000):
        data = faker.generate_json_payload()
        print(data)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
