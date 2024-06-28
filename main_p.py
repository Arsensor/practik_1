import random
import tkinter as tk
from tkinter import ttk, messagebox
from player_p import Player
from mafioso_p import Mafioso
from civilian_p import Civilian
from doctor_p import Doctor
from maniac_p import Maniac
from police_p import Police


def create_players(num_players):
    players = []
    names_m = [ "Арсений", "Степан", "Максим", "Александр", "Кирилл", "Виктор"]
    names_w = ["София", "Екатерина", "Арина", "Ольга", "Алина", "Светлана"]
    for i in range(num_players // 2):
        name_1 = random.choice(names_m)
        names_m.remove(name_1)
        gender =["Мужчина"]
        age = random.randint(18, 60)
        cunning = random.randint(1, 10)
        eloquence = random.randint(1, 10)
        player = Player(name_1, gender, age, cunning, eloquence)
        players.append(player)
        name_2 = random.choice(names_w)
        names_w.remove(name_2)
        gender = ["Женщина"]
        age = random.randint(18, 60)
        cunning = random.randint(1, 10)
        eloquence = random.randint(1, 10)
        player = Player(name_2, gender, age, cunning, eloquence)
        players.append(player)
    return players


class MafiaGame:
    def __init__(self, num_players):
        self.players_frame = None
        self.players = create_players(num_players)
        self.assign_roles()
        self.mafia_members = [p for p in self.players if isinstance(p.role, Mafioso)]
        self.civilians = [p for p in self.players if isinstance(p.role, Civilian)]
        self.police = [p for p in self.civilians if isinstance(p.role, Police)]
        self.doctor = [p for p in self.civilians if isinstance(p.role, Doctor)]
        self.clear_players = []
        self.root = tk.Tk()
        self.root.title("Игра Мафия")
        self.create_gui()
        self.night = True
        self.current_phase = "Ночь"
        self.update_phase_label()

    def assign_roles(self):
        mafia_count = max(1, len(self.players) // 4)
        mafia_members = random.sample(self.players, mafia_count)
        for player in mafia_members:
            player.role = Mafioso(player.name, player.gender, player.age, player.cunning, player.eloquence)
        civilians = [p for p in self.players if p not in mafia_members]
        doctor = random.choice(civilians)
        doctor.role = Doctor(doctor.name, doctor.gender, doctor.age, doctor.cunning, doctor.eloquence)
        civilians.remove(doctor)

        if len(civilians) >= 1:
            maniac = random.choice(civilians)
            maniac.role = Maniac(maniac.name, maniac.gender, maniac.age, maniac.cunning, maniac.eloquence)
            civilians.remove(maniac)

        if len(civilians) >= 1:
            police = random.choice(civilians)
            police.role = Police(police.name, police.gender, police.age, police.cunning, police.eloquence)
            civilians.remove(police)

        for civilian in civilians:
            civilian.role = Civilian(civilian.name, civilian.gender, civilian.age, civilian.cunning, civilian.eloquence)

    def create_gui(self):
        self.root.geometry("1480x600")
        self.players_frame = ttk.LabelFrame(self.root, text="Игроки")
        self.players_frame.pack(padx=10, pady=10, fill="x")
        columns = ("Name", "Gender", "Age", "Cunning", "Eloquence", "Role")
        self.players_tree = ttk.Treeview(self.players_frame, columns=columns, show="headings")
        self.players_tree.heading("Name", text="Имя")
        self.players_tree.heading("Gender", text="Пол")
        self.players_tree.heading("Age", text="Возраст")
        self.players_tree.heading("Cunning", text="Хитрость")
        self.players_tree.heading("Eloquence", text="Красноречие")
        self.players_tree.heading("Role", text="Роль")
        self.players_tree.pack(side="left", fill="both", expand=True)
        players_scrollbar = ttk.Scrollbar(self.players_frame, orient="vertical", command=self.players_tree.yview)
        players_scrollbar.pack(side="right", fill="y")
        self.players_tree.configure(yscrollcommand=players_scrollbar.set)
        self.action_frame = ttk.LabelFrame(self.root, text="Действия")
        self.action_frame.pack(padx=10, pady=10, fill="x")
        self.action_label = ttk.Label(self.action_frame, text="Ночь. Мафия проснулась.")
        self.action_label.pack(pady=5)
        self.action_button = ttk.Button(self.action_frame, text="Следующий ход", command=self.next_turn)
        self.action_button.pack(pady=5)
        self.log_frame = ttk.LabelFrame(self.root, text="Лог игры")
        self.log_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.log_text = tk.Text(self.log_frame, wrap="word", state="disabled")
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar = ttk.Scrollbar(self.log_frame, orient="vertical", command=self.log_text.yview)
        log_scrollbar.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        self.new_game_button = ttk.Button(self.action_frame, text="Новая игра", command=self.start_new_game)
        self.new_game_button.pack(pady=5)

    def start_new_game(self):
        self.players = create_players(len(self.players))
        self.assign_roles()
        self.mafia_members = [p for p in self.players if isinstance(p.role, Mafioso)]
        self.civilians = [p for p in self.players if isinstance(p.role, Civilian)]
        self.police = [p for p in self.civilians if isinstance(p.role, Police)]
        self.night = True
        self.current_phase = "Ночь"
        self.update_phase_label()
        self.update_players_tree()
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state="disabled")

    def update_phase_label(self):
        self.action_label.config(text=self.current_phase)

    def next_turn(self):
        if self.night:
            self.mafia_turn()
            self.maniac_turn()
        else:
            self.civilian_turn()

    def mafia_turn(self):
        alive_players = [p for p in self.players if p.alive and not isinstance(p.role, Mafioso)]
        mafia_players = [p for p in self.players if isinstance(p.role, Mafioso)]
      
        if mafia_players:
            victim = random.choice(alive_players)
            victim.is_killed = True
            self.log_message(f"Мафия убила {victim.name}.")

    def maniac_turn(self):
        alive_players = [p for p in self.players if p.alive and not isinstance(p.role, Maniac)]
        maniac_players = [p for p in self.players if p.alive and isinstance(p.role, Maniac)]

        if maniac_players:
            victim = random.choice(alive_players)
            victim.is_killed = True
            self.log_message(f"Маньяк убил {victim.name}.")
        self.night = False
        self.current_phase = "День"
        self.update_phase_label()

    def civilian_turn(self):
        if self.police:
            police_player = self.police[0]
            players_to_check = [p for p in self.players if
                                p.alive and not isinstance(p.role, Police) and p not in self.clear_players]
            if police_player.alive:
                mafia_member = random.choice(players_to_check)
                if isinstance(mafia_member.role, Mafioso):
                    self.log_message(f"Полицейский {police_player.name} разоблачил {mafia_member.name} как мафиози!")
                    mafia_member.alive = False
                    self.update_players_tree()
                elif isinstance(mafia_member.role, Maniac):
                    self.log_message(f"Полицейский {police_player.name} разоблачил {mafia_member.name} как маньяка!")
                    mafia_member.alive = False
                    self.update_players_tree()
                else:
                    self.log_message(
                        f"Полицейский {police_player.name} проверил игрока {mafia_member.name}. Он чист")
                    self.clear_players.append(mafia_member)

        for player in self.players:
            if isinstance(player.role, Doctor) and player.alive:
                alive_civilians = [p for p in game.civilians if p.alive]
                if alive_civilians:
                    revived_player = random.choice(alive_civilians)
                    if revived_player.is_killed:
                        revived_player.is_killed = False
                        game.log_message(f"Доктор {player.name} воскресил {revived_player.name}.")
                    else:
                        game.log_message(f"Доктор {player.name} выбрал не того")

        for player in [p for p in game.civilians if p.alive]:
            if player.is_killed:
                player.alive = False

        self.update_players_tree()
        self.vote_for_suspect()
        self.night = True
        self.current_phase = "Ночь"
        self.update_phase_label()

    def vote_for_suspect(self):
        is_over = self.check_game_over()
        if is_over:
            return
        alive_players = [p for p in self.players if p.alive]
        votes = {}
        for player in alive_players:
            is_voted = False
            players_to_vote = [p for p in alive_players if p != player and p not in self.clear_players]
            random.shuffle(players_to_vote)
            for player_to_vote in players_to_vote:
                if player.eloquence > player_to_vote.cunning:
                    votes[player_to_vote] = votes.get(player_to_vote, 0) + 1
                    is_voted = True
                    break
            if not is_voted:
                player_to_vote = random.choice(players_to_vote)
                votes[player_to_vote] = votes.get(player_to_vote, 0) + 1
        majority = (len(alive_players) // 2) + 1
        max_votes = max(votes.values(), default=0)
        if max_votes >= majority:
            executed_players = []
            for player, vote_count in votes.items():
                if vote_count == max_votes:
                    player.alive = False
                    executed_players.append(player)
                    break
            self.update_players_tree()
            for executed_player in executed_players:
                self.log_message(f"{executed_player.name} был казнен.")
                self.update_players_tree()

        else:
            self.log_message("Подозреваемый оправдан.")

        if not [p for p in self.players if p.alive and isinstance(p.role, (Maniac, Mafioso))]:
            self.end_game("Победили мирные жители")
            return

    def check_game_over(self):
        alive_mafia = [p for p in self.players if p.alive and isinstance(p.role, Mafioso)]
        alive_maniac = [p for p in self.players if p.alive and isinstance(p.role, Maniac)]
        alive_police = [p for p in self.players if p.alive and isinstance(p.role, Police)]
        alive_doctor = [p for p in self.players if p.alive and isinstance(p.role, Doctor)]
        alive_civilians = [p for p in self.players if
                           p.alive and isinstance(p.role, Civilian) and not isinstance(p.role, Police or Doctor)]
        is_over = False
        print(len(alive_mafia), len([p for p in self.players if p.alive and not isinstance(p.role, Mafioso)]))
        if (len(alive_mafia) == len(alive_maniac) and len(alive_civilians) == 0 and len(alive_police) == 0 and len(
                alive_doctor) == 0) or (
                len(alive_mafia) == len(alive_police) and len(alive_maniac) == 0 and len(alive_civilians) == 0 and len(
                alive_doctor) == 0) or len(alive_maniac) == len(alive_police) and len(alive_mafia) == 0 and len(
                alive_civilians) == 0 and len(alive_doctor) == 0:
            self.end_game("Ничья!")
            is_over = True
        elif len(alive_mafia) == 0 and len(alive_maniac) == 0:
            self.end_game("Мирные жители победили!")
            is_over = True
        elif len(alive_maniac) == 0 and (len(alive_civilians) <= len(alive_mafia) and len(alive_police) == 0) or len(
                alive_mafia) > len([p for p in self.players if p.alive and not isinstance(p.role, Mafioso)]):
            self.end_game("Мафия победила!")
            is_over = True
        elif len(alive_mafia) == 0 and (len(alive_civilians) <= len(alive_maniac) and len(alive_police) == 0):
            self.end_game("Маньяк победил!")
            is_over = True
        print(len(alive_doctor), len(alive_police), len(alive_civilians), len(alive_mafia), len(alive_maniac))
        return is_over

    def end_game(self, message):
        self.log_message(message)
        messagebox.showinfo("Игра окончена", message)
        self.new_game_button.pack(pady=5)

    def log_message(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.configure(state="disabled")
        self.log_text.yview(tk.END)

    def update_players_tree(self):
        self.players_tree.delete(*self.players_tree.get_children())
        for i, player in enumerate([p for p in self.players if p.alive]):
            self.players_tree.insert("", "end", iid=str(i), text=str(i), values=(
                player.name, player.gender, player.age, player.cunning, player.eloquence, player.role.role))


num_players = 8
game = MafiaGame(num_players)
game.root.mainloop()
