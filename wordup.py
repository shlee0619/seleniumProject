import os

def wordup(file_path, target):
  dict = {}

  try:
      with open(file_path, 'r', encoding='utf-8') as file:
          content = file.read()
          for word in target:
              count = content.lower().count(word.lower())
              dict[word] = count
  except FileNotFoundError:
      print(f"'{file_path}'가 안보이네요")

  return dict

target_words = ['폴리', '캔디', '태아', '낙태']
file_path = os.path.abspath('로빈쿡 메스.txt')

result = wordup(file_path, target_words)
print(result)