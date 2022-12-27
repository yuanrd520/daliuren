from contextlib import contextmanager, redirect_stdout
from io import StringIO

import pendulum as pdlm
import streamlit as st

import kinliuren
import kinqimen

from sxtwl import fromSolar


@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write

        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret

        stdout.write = new_write
        yield


def lunar_date_d(y, m, d):
    day = fromSolar(y, m, d)
    return {"月": str(day.getLunarMonth()) + "月", "日": str(day.getLunarDay())}


st.set_page_config(layout="wide", page_title="归壹 - 大六壬排盘")
pan, example = st.tabs([' 排盘 ', ' 案例 '])
with st.sidebar:
    pp_date = st.date_input("日期", pdlm.now(tz='Asia/Shanghai').date())
    pp_time = st.time_input("时间", pdlm.now(tz='Asia/Shanghai').time())
    p = str(pp_date).split("-")
    pp = str(pp_time).split(":")
    y = int(p[0])
    m = int(p[1])
    d = int(p[2])
    h = int(pp[0])
    min = int(pp[1])

with pan:
    st.header('大六壬排盘')
    cm = dict(zip(list(range(1, 13)), list("正二三四五六七八九十") + ["十一", "十二"])).get(
        int(lunar_date_d(y, m, d).get("月").replace("月", "")))
    qgz = kinqimen.Qimen1(y, m, d, h).gangzhi()
    jq = kinqimen.Qimen1(y, m, d, h).find_jieqi()
    ltext = kinliuren.Liuren(jq, cm, qgz[2], qgz[3]).result(0)
    output2 = st.empty()
    with st_capture(output2.code):
        print("{}年{}月{}日{}时".format(y, m, d, h))
        print("{} | 节气:{} | {}课 \n".format(ltext.get("日期"), ltext.get("节气"), ltext.get("格局")[0]))
        print("　　　{}".format("".join(ltext.get("三传").get("初传"))))
        print("　　　{}".format("".join(ltext.get("三传").get("中传"))))
        print("　　　{}\n".format("".join(ltext.get("三传").get("末传"))))
        print("　　　{}".format("".join([ltext.get("四课").get(i)[0][0] for i in ['四课', '三课', '二课', '一课']])))
        print("　　　{}\n".format("".join([ltext.get("四课").get(i)[0][1] for i in ['四课', '三课', '二课', '一课']])))
        print("　　　{}".format("".join([ltext.get("地转天将").get(i) for i in list("巳午未申")])))
        print("　　　{}".format("".join([ltext.get("地转天盘").get(i) for i in list("巳午未申")])))
        print("　　{}{}　　{}{}".format(ltext.get("地转天将").get("辰"), ltext.get("地转天盘").get("辰"),
                                    ltext.get("地转天盘").get("酉"), ltext.get("地转天将").get("酉")))
        print("　　{}{}　　{}{}".format(ltext.get("地转天将").get("卯"), ltext.get("地转天盘").get("卯"),
                                    ltext.get("地转天盘").get("戌"), ltext.get("地转天将").get("戌")))
        print("　　　{}".format("".join([ltext.get("地转天盘").get(i) for i in list("寅丑子亥")])))
        print("　　　{}".format("".join([ltext.get("地转天将").get(i) for i in list("寅丑子亥")])))
    expander = st.expander("原始码")
    expander.write(str(ltext))

# 隐藏made with streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
