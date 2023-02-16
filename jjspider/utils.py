import re

def chinese_to_number(chinese_num):
  """
  Convert Chinese numerical characters to their corresponding numerical values.
  """
  chinese_to_arabic = {
    '〇': 0,
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,
  }
  
  pattern = re.compile(r'([〇一二三四五六七八九]+)([十百千万亿]?)')
  result = pattern.findall(chinese_num)
  number = 0
  
  for chinese_digit, chinese_unit in result:
      digit = chinese_to_arabic[chinese_digit]
      unit = 1
      
      if chinese_unit == '十':
          unit = 10
      elif chinese_unit == '百':
          unit = 100
      elif chinese_unit == '千':
          unit = 1000
      elif chinese_unit == '万':
          unit = 10000
      elif chinese_unit == '亿':
          unit = 100000000
      
      number += digit * unit
  
  return number

def split_yc(novelclass):
  if novelclass.count('-')==3:
    return novelclass.split('-')[0]
  return None

def split_xx(novelclass):
  if novelclass.count('-')==3:
    return novelclass.split('-')[1]
    # rules = {'言情':'BG','纯爱':'BL'}
    # if _xx:
    #   return rules.get(_xx)
  return None

def split_era(novelclass):
  if novelclass.count('-')==3:
    return novelclass.split('-')[2]
  return None