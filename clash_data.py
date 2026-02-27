
import json
import os
import re

DATA_DIR = r"c:\Users\User\zhiku\clashofclansjson"

MAPPING = {
    # Buildings (Home Village)
    "大本营": "Town Hall",
    "城墙": "Wall",
    "加农炮": "Cannon",
    "箭塔": "Archer Tower",
    "迫击炮": "Mortar",
    "防空火箭": "Air Defense",
    "法师塔": "Wizard Tower",
    "空气炮": "Air Sweeper",
    "特斯拉电磁塔": "Hidden Tesla",
    "炸弹塔": "Bomb Tower",
    "X连弩": "X-Bow",
    "地狱之塔": "Inferno Tower",
    "天鹰火炮": "Eagle Artillery",
    "投石炮": "Scattershot",
    "建筑工人小屋": "Builder's Hut",
    "法术塔": "Spell Tower",
    "巨石碑": "Monolith",
    "跳弹加农炮": "Ricochet Cannon",
    "多人箭塔": "Multi-Archer Tower",
    "火焰喷射器": "Flame Flinger", # Note: Flame Flinger is a Siege Machine but listed in Defense in app.py? Or maybe Ricochet Cannon?
    "复合机械塔": "Ricochet Cannon", # Guess
    "复仇之塔": "Spell Tower", # Guess
    "超级法师塔": "Wizard Tower", # Maybe Super Wizard Tower? Not standard.
    
    # Resources
    "金圣水收集器": "Elixir Collector",
    "暗黑重油钻井": "Dark Elixir Drill",
    "储金罐": "Gold Storage",
    "圣水瓶": "Elixir Storage",
    "暗黑重油罐": "Dark Elixir Storage",
    "部落城堡": "Clan Castle",
    
    # Army Buildings
    "兵营": "Army Camp",
    "训练营": "Barracks",
    "暗黑训练营": "Dark Barracks",
    "实验室": "Laboratory",
    "法术工厂": "Spell Factory",
    "暗黑法术工厂": "Dark Spell Factory",
    "攻城机器工坊": "Workshop",
    "战宠小屋": "Pet House",
    "铁匠铺": "Blacksmith",
    "英雄殿堂": "Altar", # Not exact match usually
    
    # Traps (Some might not be in buildings.json, but mapping is here)
    "隐形炸弹": "Bomb",
    "隐形弹簧": "Spring Trap",
    "空中炸弹": "Air Bombs", # Corrected from "Air Bomb"
    "巨型炸弹": "Giant Bomb",
    "搜空地雷": "Seeking Air Mine",
    "骷髅陷阱": "Skeleton Trap",
    "飓风陷阱": "Tornado Trap",
    "终极炸弹": "Mega Mine",
    
    # Siege Machines
    "攻城战车": "Wall Wrecker",
    "攻城飞艇": "Battle Blimp",
    "攻城气球": "Stone Slammer",
    "攻城训练营": "Siege Barracks",
    "攻城滚木车": "Log Launcher",
    "攻城烈焰车": "Flame Flinger",
    "攻城钻机": "Battle Drill",
    
    # Builder Base
    "双管加农炮": "Double Cannon",
    "多管迫击炮": "Multi Mortar",
    "撼地巨石": "Crusher",
    "守卫岗哨": "Guard Post",
    "空中炸弹发射器": "Air Bombs",
    "熔岩火炮": "Roaster",
    "巨型加农炮": "Giant Cannon",
    "超级特斯拉电磁塔": "Mega Tesla",
    "熔岩发射器": "Lava Launcher",
    "建筑大师训练营": "Builder Barracks",
    "预备营": "Reinforcement Camp",
    "星空实验室": "Star Laboratory",
    "治疗小屋": "Healing Hut",
    "宝石矿井": "Gem Mine",
    "钟楼": "Clock Tower",
    "战争机器": "Battle Machine",
    "战斗直升机": "Battle Copter",
    "奥托前哨": "O.T.T.O's Outpost",
    
    # Super Troops
    "超级野蛮人": "SuperBarbarian",
    "超级弓箭手": "SuperArcher",
    "超级巨人": "SuperGiant",
    "隐秘哥布林": "SuperGoblin",
    "超级炸弹人": "SuperWallbreaker",
    "火箭气球兵": "SuperBalloon",
    "超级法师": "SuperWizard",
    "超级飞龙": "SuperDragon",
    "地狱飞龙": "InfernoDragon",
    "超级矿工": "SuperMiner",
    "超级大雪怪": "SuperYeti", # Check if exists
    "超级亡灵": "SuperMinion",
    "超级野猪骑士": "SuperHogRider",
    "超级瓦基丽武神": "SuperValkyrie",
    "超级女巫": "SuperWitch",
    "寒冰猎犬": "IceHound",
    "超级巨石投手": "SuperBowler",
    
    # Spells (Mapping Chinese to English if needed)
    "复苏法术": "Recall Spell", # Maybe? Or Revive? Recall is "回溯法术"
    "图腾法术": "Overgrowth Spell", # Guess
    "冰障法术": "Bag of Frostmites", # Maybe?
}

class ClashData:
    def __init__(self):
        self.data = {}
        self.load_all_data()

    def load_all_data(self):
        files = {
            "buildings": "buildings.json",
            "troops": "troops.json",
            "spells": "spells.json",
            "heroes": "heroes.json",
            "supers": "supers.json",
            "pets": "pets.json",
            "hero_equipment": "hero_equipment.json"
        }
        
        for key, filename in files.items():
            path = os.path.join(DATA_DIR, filename)
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        self.data[key] = json.load(f)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

    def get_data(self, item_name):
        """
        Search for item data across all loaded JSONs.
        item_name can be Chinese or English (e.g. "野蛮人 (Barbarian)").
        """
        search_key = self._extract_key(item_name)
        
        if not search_key:
            return None

        # Search order
        # 1. Try exact match in all files
        for category in self.data:
            if search_key in self.data[category]:
                return self.data[category][search_key]
        
        # 2. Try partial match or other variations if needed
        # (For now, strict match based on extraction/mapping is safer)
        
        return None

    def _extract_key(self, item_name):
        # 1. Check if English name is in parentheses
        match = re.search(r'\((.*?)\)', item_name)
        if match:
            return match.group(1).strip()
        
        # 2. Check mapping
        clean_name = item_name.strip()
        if clean_name in MAPPING:
            return MAPPING[clean_name]
        
        # 3. If it looks like English, return as is
        if re.match(r'^[A-Za-z\s\.\-\']+$', clean_name):
            return clean_name
            
        return None

