import re

def chinese_to_number(chinese_num):
  """
  Convert Chinese numerical characters to their corresponding numerical values.
  """
  pattern = re.compile(r'([0-9]+)([十百千万亿]?)')
  result = pattern.search(chinese_num)
  number = 0
  digit = result[0]
  unit = 1
  if result[-1] == '十':
    unit = 10
  elif result[-1] == '百':
    unit = 100
  elif result[-1] == '千':
    unit = 1000
  elif result[-1] == '万':
    unit = 10000
  elif result[-1] == '亿':
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