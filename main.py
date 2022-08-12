import os.path
from typing import *


class Log_in_out_msg:
    def __init__(self, player, is_in, time):
        self.player: str = player
        self.is_in: bool = is_in
        self.time: str = time


def parse_login_log(s: str) -> Optional[Log_in_out_msg]:
    if "joined the game" not in s:
        return None
    tokens = s.split()
    player = tokens[3]
    time = tokens[0][1:-1]
    return Log_in_out_msg(player, True, time)


def parse_logout_log(s: str) -> Optional[Log_in_out_msg]:
    if "left the game" not in s:
        return None
    tokens = s.split()
    player = tokens[3]
    time = tokens[0][1:-1]
    return Log_in_out_msg(player, False, time)


def stat_one_day(filename):
    with open(filename, encoding="UTF-8") as file:
        lines = file.readlines()
        msgs = []
        for line in lines:
            if in_msg := parse_login_log(line):
                if not in_msg.player.startswith("bot_"):
                    msgs.append(in_msg)
                    continue
            if out_msg := parse_logout_log(line):
                if not out_msg.player.startswith("bot_"):
                    msgs.append(out_msg)
                    continue
        players = set()
        res = []
        for msg in msgs:
            if msg.is_in:
                players.add(msg.player)
                res.append((msg.time, players.copy()))
                continue
            else:
                if msg.player in players:
                    players.remove(msg.player)
                    res.append((msg.time, players.copy()))
                    continue
        return res


def gen_report(res, filename):
    report_path = os.path.join("./report", filename + ".txt")
    with open(report_path, mode="wt", encoding="UTF-8") as file:
        for time, player_set in res:
            buffer = f"[{time}] "

            players = list(player_set)
            players_str = ""
            for player in players:
                players_str += f"{player}, "

            if players_str != "":
                players_str = players_str[0:-2]
            else:
                players_str = "无玩家在线"

            buffer += players_str
            file.write(buffer + "\n")


if __name__ == "__main__":
    file_list = os.listdir("./logs")
    for file_name in file_list:
        print(file_name)
        res = stat_one_day(f"./logs/{file_name}")
        gen_report(res, os.path.splitext(file_name)[0])


