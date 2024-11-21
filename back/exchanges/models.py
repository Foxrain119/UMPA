from django.db import models

# Create your models here.
class Exchange(models.Model):
  cur_unit = models.CharField(max_length=10)          # 통화코드
  cur_nm = models.CharField(max_length=30)            # 국가/통화명
  ttb = models.FloatField()                           # 전신환(송금) 받으실때	
  tts = models.FloatField()                           # 전신환(송금) 보내실때	
  deal_bas_r = models.FloatField()                    # 매매 기준율
  bkpr = models.FloatField()                          # 장부가격
  kftc_deal_bas_r = models.FloatField()               # 서울외국환중개 매매 기준율
  kftc_bkpr = models.FloatField()                     # 서울외국환중개 장부가격
  # yy_efee_r = models.TextField()                    # 년환가료율
  # ten_dd_efee_r = models.TextField()                # 10일환가료율
