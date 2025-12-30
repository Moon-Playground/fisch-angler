import os
import tomllib
import tomlkit


class Config:
    def load_config(self):
        default_config = {
            "ocr": {
                "capture_width": 124,
                "capture_height": 62,
                "capture_x": 710,
                "capture_y": 390,
                "backend": "tesseract"
            },
            "hotkeys": {
                "test_capture": "F2",
                "toggle_box": "F3",
                "toggle_action": "F4",
                "exit_app": "F5"
            },
            "ui": {
                "enable_overlay": True,
                "enable_debug": False,
                "status_x": 85,
                "status_y": 1
            },
            "coordinates": {
                "fish_area_x": 0,
                "fish_area_y": 0,
                "search_bar_x": 0,
                "search_bar_y": 0,
                "dialogue_x": 0,
                "dialogue_y": 0
            },
            "delay": {
                "loop": 30.0,
                "initial": 1.0,
                "typing": 0.05,
                "inv": 1.0,
                "action": 0.5
            },
            "misc": {
                "angler_location": "sunstone"
            }
        }
        fish_list = {
            "moosewood": ["Anchovy", "Mackerel", "Red Snapper", "Sockeye Salmon", "Trout", "Barracuda", "Yellowfin Tuna", "Eel", "Flounder", "Bull Shark", "Moonfish", "Pike", "Snook", "Bream", "Largemouth Bass", "Carp", "Goldfish", "Whiptail Catfish", "Whisker Bill", "Treble Bass"],
            "sunstone": ["Glassfish", "Sweetfish", "Chinfish", "Longtail Bass", "Red Tang", "Trumpetfish", "Mahi Mahi", "Napoleonfish", "Ancient Wood", "Sunfish", "Wiifish", "Voltfish", "Speed Core", "Tartaruga"],
            "roslit": ["Chub", "Minnow", "Pearl", "Perch", "Blue Tang", "Butterflyfish", "Clownfish", "Pumpkinseed", "Angelfish", "Clam", "Gilded Pearl", "Ribbon Eel", "Rose Pearl", "Squid", "Yellow Boxfish", "Alligator Gar", "Arapaima", "Mauve Pearl", "Suckermouth Catfish", "Axolotl", "Deep Pearl", "Dumbo Octopus", "Aurora Pearl", "Manta Ray", "Golden Sea Pearl"],
            "terrapin": ["Gudgeon", "Smallmouth Bass", "Walleye", "White Bass", "Chinook Salmon", "Redeye Bass", "King Oyster", "Golden Smallmouth Bass", "Olm", "Sea Turtle", "Manatee"],
            "depth": ["Destroyed Fossil", "Scrap Metal", "Deep-sea Dragonfish", "Deep-sea Hatchetfish", "Depth Octopus", "Frilled Shark", "Luminescent Minnow", "Three-eyed Fish", "Black Dragon Fish", "Goblin Shark", "Spider Crab", "Ancient Eel", "Nautilus", "Small Spine Chimera", "Barreleye Fish", "Mutated Shark", "Sea Snake", "Ancient Depth Serpent"],
            "ancient": ["Cladoselache", "Piranha", "Anomalocaris", "Onychodus", "Starfish", "Acanthodii", "Hyneria", "Xiphactinus", "Cobia", "Hallucigenia", "Dunkleosteus", "Floppy", "Ginsu Shark", "Leedsichthys", "Helicoprion", "Meg's Fang", "Meg's Spine", "Mosasaurus", "Ancient Megalodon", "Megalodon", "Banana"],
            "forsaken": ["Corsair Grouper", "Shortfin Mako Shark", "Buccaneer Barracuda", "Galleon Goliath", "Cutlass Fish", "Scurvy Sailfish", "Cursed Eel", "Reefrunner Snapper", "Shipwreck Barracuda", "Captain's Goldfish", "Golden Seahorse", "Pirate Captain's Goldfish"],
            "crimson": ["Red Spotted Blenny", "Red Crabsquid", "Sea Raven", "Red Fangtooth", "Viperfish", "Japanese Dragon Eel", "Vampire Squid", "Colossal Ancient Dragon", "Lithodes Megacantha"],
            "luminescent": ["Bluelip Batfish", "Hawaiian Bobtail Squid", "Dinoflagellates", "Blue Ribbon Eel", "Kitefin Shark", "Atolla Jellyfish", "Electric Blue Seahorse", "Colossal Blue Dragon", "Blue Sea Slug", "Colossal Ethereal Dragon"],
            "lostjungle": ["Cardinal Tetra", "Neon Tetra", "Bronze Corydoras", "Freshwater Pacu", "Oscar Cichlid", "Black Ghost Knifefish", "Northern Snakehead", "Payara", "Redeye Piranha", "Silver Arowana", "Electric Eel", "Piraiba", "Pirarucu", "Goliath Tigerfish", "Motoro Stingray", "Mossjaw", "Elder Mossjaw"]
        }
        default_config["fish_list"] = fish_list

        if os.path.exists("auto_shake.toml"):
            try:
                with open("auto_shake.toml", "rb") as f:
                    config = tomllib.load(f)
                
                # Ensure all keys exist
                if "ocr" not in config: config["ocr"] = default_config["ocr"]
                if "hotkeys" not in config: config["hotkeys"] = default_config["hotkeys"]
                if "ui" not in config: config["ui"] = default_config["ui"]
                if "coordinates" not in config: config["coordinates"] = default_config["coordinates"]
                if "delay" not in config: config["delay"] = default_config["delay"]
                if "misc" not in config: config["misc"] = default_config["misc"]
                if "fish_list" not in config: config["fish_list"] = default_config["fish_list"]
                
                # Check individual keys in coordinates if it exists but might be missing new ones
                for k, v in default_config["coordinates"].items():
                    if k not in config["coordinates"]:
                        config["coordinates"][k] = v
                
                # Check individual keys in fish_list
                for k, v in default_config["fish_list"].items():
                    if k not in config["fish_list"]:
                        config["fish_list"][k] = v
                        
                return config
            except Exception:
                pass

        # Save default if not exists or failed
        self.save_config_file(default_config)
        return default_config

    def save_config_coords(self):
        self.config_data["ocr"]["capture_width"] = self.capture_box.capture_width
        self.config_data["ocr"]["capture_height"] = self.capture_box.capture_height
        self.config_data["ocr"]["capture_x"] = self.capture_box.capture_x
        self.config_data["ocr"]["capture_y"] = self.capture_box.capture_y
        self.config_data["ocr"]["backend"] = self.ocr_backend
        
        if "coordinates" not in self.config_data:
            self.config_data["coordinates"] = {}

        self.config_data["coordinates"]["fish_area_x"] = self.fish_area_x
        self.config_data["coordinates"]["fish_area_y"] = self.fish_area_y
        self.config_data["coordinates"]["search_bar_x"] = self.search_bar_x
        self.config_data["coordinates"]["search_bar_y"] = self.search_bar_y
        self.config_data["coordinates"]["dialogue_x"] = self.dialogue_x
        self.config_data["coordinates"]["dialogue_y"] = self.dialogue_y
        
        self.save_config_file(self.config_data)

    def save_and_apply_config(self):
        # Update config data from UI
        for key, entry in self.hk_entries.items():
            self.config_data["hotkeys"][key] = entry.get()
        if self.overlay_var.get() != self.enable_overlay:
            self.enable_overlay = self.overlay_var.get()
            if self.enable_overlay:
                self.show_status_window()
            else:
                self.hide_status_window()
        self.config_data["ui"]["enable_overlay"] = self.overlay_var.get()
        self.save_config_file(self.config_data)
        self.apply_hotkeys()

    def save_config_file(self, config):
        with open("auto_shake.toml", "w") as f:
            tomlkit.dump(tomlkit.parse(tomlkit.dumps(config)), f)
