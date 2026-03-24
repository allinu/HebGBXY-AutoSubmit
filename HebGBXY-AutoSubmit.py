import requests
from bs4 import BeautifulSoup
import re
import json
import time
from datetime import datetime
import threading
import warnings
import urllib3

# ========== 配置常量 ==========
# INFO 请根据实际情况修改以下配置

# TODO SESSION cookie值
SESSION = ""

# TODO 课程列表URL
URL = ""

# 请求头配置
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
REFERER = "https://www.hebgb.gov.cn/student/class_myClassList.do?type=1&menu=myclass"

# 请求延迟（秒），避免请求过快被封
REQUEST_DELAY = 10

# 默认视频时长（秒），当无法解析到分钟数时使用
DEFAULT_DURATION = 1800

# SSL证书验证（如果遇到证书错误，可以设置为False）
VERIFY_SSL = False

# 禁用SSL警告
if not VERIFY_SSL:
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========== 功能函数 ==========


def print_output(message):
    """输出信息到控制台"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def submit_data():
    """提交数据的主函数"""
    headers = {
        "Cookie": f"SESSION={SESSION}",
        "User-Agent": USER_AGENT,
        "Referer": REFERER,
    }

    print_output("开始处理课程...")
    thread = threading.Thread(target=process_requests, args=(SESSION, URL, headers))
    thread.start()
    thread.join()  # 等待线程完成


def process_requests(SESSION, url, headers):
    """处理请求的核心逻辑"""
    try:
        response = requests.get(url, headers=headers, verify=VERIFY_SSL)
        response.encoding = "utf-8"

        soup = BeautifulSoup(response.text, "html.parser")

        records = []

        for div in soup.select("div.hoz_course_row"):
            onclick_btn = div.select_one("input.hover_btn")
            if not onclick_btn or "onclick" not in onclick_btn.attrs:
                continue

            # 将onclick属性值转换为字符串
            onclick_value = str(onclick_btn["onclick"])
            match_id = re.search(r"addUrl\((\d+)\)", onclick_value)
            if not match_id:
                continue
            video_id = int(match_id.group(1))

            course_link = div.select_one("a[href*='course_detail.do']")
            if not course_link or "href" not in course_link.attrs:
                continue

            # 将href属性值转换为字符串
            href_value = str(course_link["href"])
            match_course = re.search(r"courseId=(\d+)", href_value)
            if not match_course:
                continue
            course_id = int(match_course.group(1))

            time_span = div.select_one("span:-soup-contains('分钟')")
            duration = DEFAULT_DURATION  # 使用配置的默认时长
            if time_span:
                match_time = re.search(r"(\d+)\s*分钟", time_span.text)
                if match_time:
                    duration = int(match_time.group(1)) * 60

            records.append(
                {"id": video_id, "study_course": course_id, "duration": duration}
            )

        print_output(f"找到 {len(records)} 个课程记录")

        if not records:
            print_output("未找到任何课程记录，请检查URL和SESSION配置")
            return

        common_headers = {
            "User-Agent": USER_AGENT,
            "Cookie": f"SESSION={SESSION}",
        }

        success_count = 0
        fail_count = 0

        for i, record in enumerate(records, 1):
            id_ = record["id"]
            course = record["study_course"]
            duration = record["duration"]
            timestamp = str(int(time.time() * 1000))

            print_output(f"处理第 {i}/{len(records)} 个课程: ID={id_}, 课程ID={course}")

            # 第一步：访问课程播放页面
            play_url = f"https://www.hebgb.gov.cn/portal/study_play.do?id={id_}"
            play_headers = {
                **common_headers,
                "Referer": "https://www.hebgb.gov.cn/portal/index.do",
            }
            play_resp = requests.get(play_url, headers=play_headers, verify=VERIFY_SSL)
            if play_resp.status_code != 200:
                print_output(
                    f"[✗] 无法访问课程页面 id={id_}，状态码：{play_resp.status_code}"
                )
                fail_count += 1
                continue

            print_output(f"课程页面 id={id_} 访问成功")

            # 第二步：获取资源清单
            manifest_url = f"https://www.hebgb.gov.cn/portal/getManifest.do?id={course}&is_gkk=false&_={timestamp}"
            manifest_headers = {
                **common_headers,
                "Referer": play_url,
                "X-Requested-With": "XMLHttpRequest",
            }
            manifest_resp = requests.get(
                manifest_url, headers=manifest_headers, verify=VERIFY_SSL
            )
            if manifest_resp.status_code != 200:
                print_output(
                    f"[✗] 无法获取资源清单 course={course}，状态码：{manifest_resp.status_code}"
                )
                fail_count += 1
                continue

            print_output(f"资源清单 course={course} 获取成功")

            # 第三步：提交学习记录
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            serialize_sco = {
                "res01": {
                    "lesson_location": duration,
                    "session_time": duration,
                    "last_learn_time": now_time,
                },
                "last_study_sco": "res01",
            }
            post_data = {
                "id": str(id_),
                "serializeSco": json.dumps(serialize_sco, separators=(",", ":")),
                "duration": str(duration),
                "study_course": str(course),
            }
            post_headers = {
                **common_headers,
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": play_url,
                "Origin": "https://www.hebgb.gov.cn",
            }
            post_url = "https://www.hebgb.gov.cn/portal/seekNew.do"
            post_resp = requests.post(
                post_url, headers=post_headers, data=post_data, verify=VERIFY_SSL
            )

            if post_resp.status_code == 200:
                print_output(f"[✓] 提交记录 ID={id_}, 课程={course} 成功")
                success_count += 1
            else:
                print_output(
                    f"[✗] 提交记录 ID={id_}, 课程={course} 失败，状态码：{post_resp.status_code}"
                )
                if len(post_resp.text) > 0:
                    print_output(f"返回内容：{post_resp.text[:200]}...")
                fail_count += 1

            # 请求延迟，避免请求过快被封
            if i < len(records):  # 最后一个不需要延迟
                time.sleep(REQUEST_DELAY)

        print_output("=" * 50)
        print_output(
            f"处理完成: 成功 {success_count} 个，失败 {fail_count} 个，总计 {len(records)} 个"
        )
        print_output("=" * 50)

    except requests.exceptions.RequestException as e:
        print_output(f"网络请求异常: {str(e)}")

    except Exception as e:
        print_output(f"处理发生异常: {str(e)}")


# ========== 主程序入口 ==========
if __name__ == "__main__":
    print_output("河北网络干部学院自动提交程序启动")
    print_output("=" * 50)
    print_output(f"SESSION: {SESSION[:20]}...")
    print_output(f"URL: {URL}")
    print_output(f"User-Agent: {USER_AGENT[:50]}...")
    print_output(f"请求延迟: {REQUEST_DELAY}秒")
    print_output(f"默认时长: {DEFAULT_DURATION}秒")
    print_output("=" * 50)

    # 检查配置
    if SESSION == "your_session_cookie_here":
        print_output("[警告] 请先修改代码开头的SESSION配置为您的实际SESSION值")
        print_output("[提示] 可以通过浏览器开发者工具获取SESSION cookie")
    else:
        submit_data()
