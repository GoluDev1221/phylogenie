from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from Bio import Entrez
import random

Entrez.email = "djsurda1221@gmail.com"

class AnalysisScreen(Screen):
    def __init__(self, **kwargs):
        super(AnalysisScreen, self).__init__(**kwargs)

        main_layout = BoxLayout(orientation='vertical', spacing=20, padding=20)

        logo_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        logo = Image(source='analysis_title_image.png', size_hint=(None, None), size=(300, 300))
        logo_layout.add_widget(logo)
        main_layout.add_widget(logo_layout)

        input_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), width=400, height=40, spacing=10)
        input_layout.pos_hint = {'center_x': 0.5}
        self.species_input1 = TextInput(hint_text="Enter First Species Name", size_hint=(1, None), height=40, font_size=14)
        self.species_input2 = TextInput(hint_text="Enter Second Species Name", size_hint=(1, None), height=40, font_size=14)
        input_layout.add_widget(self.species_input1)
        input_layout.add_widget(self.species_input2)
        main_layout.add_widget(input_layout)

        random_button_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.random_button = Button(
            text="Select Random Species",
            size_hint=(0.3, 0.8),
            background_color=(0.1, 0.6, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=25,
            on_press=self.select_random_species_pair
        )
        random_button_layout.add_widget(self.random_button)
        main_layout.add_widget(random_button_layout)

        query_button_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.query_button = Button(
            text="Find Common Taxon",
            size_hint=(0.3, 0.7),
            background_color=(0.1, 0.6, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=25,
            on_press=self.perform_comparison
        )
        query_button_layout.add_widget(self.query_button)
        main_layout.add_widget(query_button_layout)

        self.output_area = ScrollView(size_hint=(1, None), height=300)
        self.output_label = Label(size_hint_y=None, text="Results will be shown here.", font_size=30, valign='top', halign='center')
        self.output_label.bind(texture_size=self.update_output_height)
        self.output_area.add_widget(self.output_label)
        main_layout.add_widget(self.output_area)

        back_button_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(400, 100), padding=10)
        back_button_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.back_button = Button(
            text="Back",
            size_hint=(1, 1),
            size=(200, 50),
            font_size=30,
            background_color=(0, 0, 0.5, 1),
            color=(1, 1, 1, 1),
            on_press=self.go_back
        )
        back_button_layout.add_widget(self.back_button)
        main_layout.add_widget(back_button_layout)

        self.add_widget(main_layout)

    def perform_comparison(self, instance):
        species1 = self.species_input1.text.strip()
        species2 = self.species_input2.text.strip()

        if species1 and species2:
            self.output_label.text = "Fetching taxonomy for both species... Please wait."
            lineage1 = self.query_taxonomy(species1)
            lineage2 = self.query_taxonomy(species2)

            if lineage1 is None:
                self.output_label.text = f"Error: Could not find results for {species1}. Please check the name and try again."
                return
            if lineage2 is None:
                self.output_label.text = f"Error: Could not find results for {species2}. Please check the name and try again."
                return

            common_taxon = self.find_lowest_common_taxon(lineage1, lineage2)
            if common_taxon:
                self.output_label.text = f"Common taxon between {species1} and {species2}:\n\n{common_taxon}" 
            else:
                self.output_label.text = "No common taxon found."
        else:
            self.output_label.text = "Please enter valid names for both species."

    def query_taxonomy(self, species):
        try:
            handle = Entrez.esearch(db="taxonomy", term=species)
            result = Entrez.read(handle)
            handle.close()

            if not result['IdList']:
                return None

            taxon_id = result['IdList'][0]
            handle = Entrez.efetch(db="taxonomy", id=taxon_id, retmode="xml")
            result = Entrez.read(handle)
            handle.close()

            lineage = result[0]['Lineage'].split(';')
            return lineage
        except Exception as e:
            print(f"Error fetching taxonomy for {species}: {e}")
            return None

    def find_lowest_common_taxon(self, lineage1, lineage2):
        min_length = min(len(lineage1), len(lineage2))
        for i in range(min_length):
            if lineage1[i] != lineage2[i]:
                return lineage1[i - 1] if i > 0 else None
        return lineage1[min_length - 1] if min_length > 0 else None

    def update_output_height(self, instance, value):
        self.output_label.height = value[1]

    def go_back(self, instance):
        self.manager.current = 'home'

    def select_random_species_pair(self, instance):
        species_pairs = [
    ('Panthera leo', 'Panthera tigris'),  # Lion and Tiger
    ('Homo sapiens', 'Panthera leo'),    # Human and Lion
    ('Gorilla gorilla', 'Pongo pygmaeus'), # Gorilla and Orangutan
    ('Equus ferus caballus', 'Bubalus bubalis'),  # Horse and Water Buffalo
    ('Canis lupus', 'Vulpes vulpes'),  # Gray Wolf and Red Fox
    ('Ursus arctos', 'Ursus maritimus'),  # Brown Bear and Polar Bear
    ('Panthera onca', 'Acinonyx jubatus'),  # Jaguar and Cheetah
    ('Loxodonta africana', 'Elephas maximus'),  # African Elephant and Asian Elephant
    ('Delphinus delphis', 'Tursiops truncatus'),  # Common Dolphin and Bottlenose Dolphin
    ('Balaenoptera musculus', 'Megaptera novaeangliae'),  # Blue Whale and Humpback Whale
    ('Grizzly bear', 'Black bear'),  # Grizzly Bear and Black Bear
    ('Equus zebra', 'Equus quagga'),  # Zebra and Plains Zebra
    ('Falco peregrinus', 'Haliaeetus leucocephalus'),  # Peregrine Falcon and Bald Eagle
    ('Lynx lynx', 'Felis catus'),  # Eurasian Lynx and Domestic Cat
    ('Rangifer tarandus', 'Cervus elaphus'),  # Reindeer and Red Deer
    ('Carcharodon carcharias', 'Galeocerdo cuvier'),  # Great White Shark and Tiger Shark
    ('Vulpes vulpes', 'Canis latrans'),  # Red Fox and Coyote
    ('Ailuropoda melanoleuca', 'Ursus maritimus'),  # Giant Panda and Polar Bear
    ('Bubalus bubalis', 'Bos taurus'),  # Water Buffalo and Cattle
    ('Panthera pardus', 'Neofelis nebulosa'),  # Leopard and Clouded Leopard
    ('Crotalus atrox', 'Crotalus viridis'),  # Western Diamondback Rattlesnake and Prairie Rattlesnake
    ('Sphenodon punctatus', 'Chelonia mydas'),  # Tuatara and Green Sea Turtle
    ('Pteropus vampyrus', 'Desmodus rotundus'),  # Flying Fox and Common Vampire Bat
    ('Lutra lutra', 'Lontra canadensis'),  # European Otter and North American River Otter
    ('Dendrobates tinctorius', 'Ranitomeya reticulata'),  # Dyeing Poison Frog and Reticulated Poison Frog
    ('Chamaeleo chamaeleon', 'Furcifer pardalis'),  # European Chameleon and Panther Chameleon
    ('Ailuropoda melanoleuca', 'Vulpes vulpes'),  # Giant Panda and Red Fox
    ('Hippopotamus amphibius', 'Crocodylus porosus'),  # Hippopotamus and Saltwater Crocodile
    ('Sula nebouxii', 'Puffinus puffinus'),  # Blue-footed Booby and Manx Shearwater
    ('Trichechus manatus', 'Dugong dugon'),  # West Indian Manatee and Dugong
    ('Gavia immer', 'Podiceps cristatus'),  # Common Loon and Great Crested Grebe
    ('Tachybaptus ruficollis', 'Grebe'),  # Little Grebe and Great Crested Grebe
    ('Salmo salar', 'Oncorhynchus mykiss'),  # Atlantic Salmon and Rainbow Trout
    ('Spheniscus demersus', 'Eudyptula minor')  # African Penguin and Little Blue Penguin
]


        random_pair = random.choice(species_pairs)
        species1, species2 = random_pair

        self.species_input1.text = species1
        self.species_input2.text = species2
