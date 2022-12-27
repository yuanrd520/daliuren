# -*- coding: utf-8 -*-
import sxtwl, re, time
import itertools
import math, datetime, re, ephem


class Qimen1:

    def __init__(self, year, month, day, hour):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.jieqi = re.findall('..',
                                '春分清明穀雨立夏小满芒种夏至小暑大暑立秋处暑白露秋分寒露霜降立冬小雪大雪冬至小寒大寒立春雨水惊蛰')
        self.jieqi_all = self.new_list(self.jieqi, "冬至")

        self.cnumber = list("一二三四五六七八九")

        self.Gan = list("甲乙丙丁戊己庚辛壬癸")
        self.Zhi = list("子丑寅卯辰巳午未申酉戌亥")


    def new_list(self, olist, o):
        zhihead_code = olist.index(o)
        res1 = []
        for i in range(len(olist)):
            res1.append(olist[zhihead_code % len(olist)])
            zhihead_code = zhihead_code + 1
        return res1


    def jq(self, year, month, day, hour):
        jd = ephem.Date(
            str(year) + "/" + str(month).zfill(2) + "/" + str(day).zfill(2) + " " + str(hour).zfill(2) + ":00:00.00")
        ct = datetime.datetime.strptime(str(year) + "-" + str(month) + "-" + str(day) + "-" + str(hour) + ":00:00",
                                        "%Y-%m-%d-%H:%M:%S")
        p = ct - datetime.timedelta(days=7)
        pp = ct - datetime.timedelta(days=21)
        bf = self.fjqs(p.year, p.month, p.day, p.hour)
        bbf = self.fjqs(pp.year, pp.month, pp.day, pp.hour)
        if ct < bf[1]:
            return bbf[0]
        else:
            return bf[0]



    def fjqs(self, year, month, day, hour):
        jd = ephem.Date(
            str(year) + "/" + str(month).zfill(2) + "/" + str(day).zfill(2) + " " + str(hour).zfill(2) + ":00:00.00")
        ct = datetime.datetime.strptime(str(year) + "-" + str(month) + "-" + str(day) + "-" + str(hour) + ":00:00",
                                        "%Y-%m-%d-%H:%M:%S")
        n = int(self.ecliptic_lon(jd) * 180.0 / math.pi / 15) + 1
        c = []
        for i in range(1):
            if n >= 24:
                n -= 24
            jd = self.iteration(jd)
            d = ephem.Date(jd + 1 / 3).tuple()
            c.append([self.jieqi[n], datetime.datetime.strptime(
                str(d[0]) + "-" + str(d[1]) + "-" + str(d[2]) + "-" + str(d[3]) + ":00:00", "%Y-%m-%d-%H:%M:%S")])
        return c[0]


    def ecliptic_lon(self, jd_utc):
        s = ephem.Sun(jd_utc)
        return ephem.Ecliptic(ephem.Equatorial(s.ra, s.dec, epoch=jd_utc)).lon


    def iteration(self, jd):
        s1 = self.sta(jd)
        s0 = s1
        dt = 1.0
        while True:
            jd += dt
            s = self.sta(jd)
            if s0 != s:
                s0 = s
                dt = -dt / 2
            if abs(dt) < 0.0000001 and s != s1:
                break
        return jd


    # 根据当前时间，求下个节气的发生时间
    def iteration11(jd, sta):  # jd：要求的开始时间，sta：不同的状态函数
        s1 = sta(jd)  # 初始状态(太阳处于什么位置)
        s0 = s1
        dt = 1.0  # 初始时间改变量设为1天
        while True:
            jd += dt
            s = sta(jd)
            if s0 != s:
                s0 = s
                dt = -dt / 2  # 使时间改变量折半减小
            if abs(dt) < 0.0000001 and s != s1:
                break
        return jd




    def sta(self, jd):
        return int(self.ecliptic_lon(jd) * 180.0 / math.pi / 15)




    # 干支
    def gangzhi(self):
        if self.hour == 23:
            d = datetime.datetime.strptime(
                str(self.year) + "-" + str(self.month) + "-" + str(self.day) + "-" + str(self.hour) + ":00:00",
                "%Y-%m-%d-%H:%M:%S") + datetime.timedelta(hours=1)

        else:
            d = datetime.datetime.strptime(
                str(self.year) + "-" + str(self.month) + "-" + str(self.day) + "-" + str(self.hour) + ":00:00",
                "%Y-%m-%d-%H:%M:%S")

        print(d)

        cdate = sxtwl.fromSolar(d.year, d.month, d.day)
        return [self.Gan[cdate.getYearGZ().tg] + self.Zhi[cdate.getYearGZ().dz],
                self.Gan[cdate.getMonthGZ().tg] + self.Zhi[cdate.getMonthGZ().dz],
                self.Gan[cdate.getDayGZ().tg] + self.Zhi[cdate.getDayGZ().dz],
                self.Gan[cdate.getHourGZ(d.hour).tg] + self.Zhi[cdate.getHourGZ(d.hour).dz]]





    # 找节气
    def find_jieqi(self):
        return self.jq(self.year, self.month, self.day, self.hour)

    # https://www.runoob.com/python/att-string-zfill.html
    def jq(self, year, month, day, hour):
        jd = ephem.Date(
            str(year) + "/" + str(month).zfill(2) + "/" + str(day).zfill(2) + " " + str(hour).zfill(2) + ":00:00.00")
        ct = datetime.datetime.strptime(str(year) + "-" + str(month) + "-" + str(day) + "-" + str(hour) + ":00:00",
                                        "%Y-%m-%d-%H:%M:%S")
        p = ct - datetime.timedelta(days=7)
        pp = ct - datetime.timedelta(days=21)
        bf = self.fjqs(p.year, p.month, p.day, p.hour)
        bbf = self.fjqs(pp.year, pp.month, pp.day, pp.hour)
        if ct < bf[1]:
            return bbf[0]
        else:
            return bf[0]




if __name__ == '__main__':
    tic = time.perf_counter()
    print(Qimen1(1980, 11, 8, 10).gangzhi())
    print(Qimen1(1980, 11, 8, 10).find_jieqi())
