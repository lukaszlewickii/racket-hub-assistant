import json
import random
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Literal


SCENARIOS_PL = [
    {
        "context": "Pytanie o zasady padla",
        "questions": [
            "Jakie są podstawowe zasady padla?",
            "Jak się gra w padla?",
            "Czym różni się padel od tenisa?",
            "Czy w padlu można używać ścian?",
            "Jak wygląda kort do padla?",
        ],
        "answers": [
            "Padel to gra 2 vs 2 na korcie otoczonym szklanymi ścianami. Serwis wykonuje się spodem, piłka musi odbić się w polu serwisowym.  Możesz używać ścian - piłka może się od nich odbijać!  Punktacja jak w tenisie: 15, 30, 40, gra.",
            "W padla gra się czwórkami (2 vs 2) na mniejszym korcie niż tenis. Kort ma szklane ściany, których można używać podczas gry. Serwis wykonuje się spodem, a punktacja jest identyczna jak w tenisie.",
            "Główne różnice: 1) Padel ma szklane ściany, których używasz w grze.  2) Kort jest mniejszy.  3) Zawsze gra się w deblu (2v2). 4) Rakieta jest solidna bez strun.  5) Piłka ma niższe ciśnienie.",
            "Tak! To jest główna cecha padla - możesz odbijać piłkę od szklanych ścian. Najpierw piłka musi odbić się od podłoża, ale potem może trafić w ścianę. Możesz też celowo zagrać w ścianę po swojej stronie.",
            "Kort do padla ma wymiary 10x20m, otoczony jest szklanymi ścianami (3m wysokości) i metalową siatką. Jest mniejszy niż kort tenisowy. Ma charakterystyczną siatkę pośrodku i oznaczone pola serwisowe.",
        ]
    },
    {
        "context": "Matchmaking i szukanie partnerów",
        "questions": [
            "Szukam kogoś do gry w padla w Warszawie",
            "Jak znaleźć partnera do squasha?",
            "Chcę zagrać dziś wieczorem, kto chętny? ",
            "Jestem początkujący, szukam kogoś na podobnym poziomie",
            "Gdzie mogę znaleźć ludzi do gry? ",
        ],
        "answers": [
            "Super! Pomogę Ci znaleźć partnera. Kilka pytań: 1) Jaki masz poziom (początkujący/średni/zaawansowany)? 2) O której chcesz grać? 3) W jakiej dzielnicy? 4) Masz już kort czy trzeba zarezerwować?",
            "Znajdę dla Ciebie partnerów do squasha! Powiedz mi:  jaki jest Twój poziom zaawansowania, kiedy chcesz grać i w jakiej lokalizacji? To pomoże mi dopasować odpowiednich graczy.",
            "Świetnie! Aby znaleźć partnera na dziś: 1) Podaj swoją lokalizację 2) Preferowaną godzinę 3) Poziom zaawansowania.  Sprawdzę kto jest dostępny w Twojej okolicy! ",
            "Doskonale, że chcesz grać z kimś na podobnym poziomie! Dla początkujących polecam: 1) Szukanie w lokalnych klubach 2) Grupy dla beginnerów 3) Lekcje z instruktorem na start. Chcesz, żebym znalazł początkujących w Twojej okolicy?",
            "Możesz znaleźć partnerów:  1) W tej aplikacji (dodaj swój profil i preferencje) 2) Lokalne kluby padla/squasha często mają tablice ogłoszeń 3) Grupy Facebook w Twoim mieście 4) Zapytaj recepcję w klubie.  Gdzie mieszkasz?",
        ]
    },
    {
        "context": "Sprzęt i wyposażenie",
        "questions": [
            "Jaką rakietę do padla polecasz dla początkujących?",
            "Co zabrać na pierwszy trening?",
            "Czy potrzebuję specjalnych butów?",
            "Jaka piłka jest używana w squashu?",
            "Ile kosztuje dobra rakieta do padla?",
        ],
        "answers":  [
            "Dla początkujących polecam rakietę o okrągłym kształcie (round shape) - jest najbardziej kontrolna. Dobry wybór to:  Bullpadel Vertex, Head Alpha, Adidas Adipower (wersje początkujące). Budżet: 300-600 zł na start.",
            "Na pierwszy trening zabierz: 1) Buty sportowe (najlepiej do tenisa/indoor) 2) Sportowy strój (koszulka, spodenki/legginsy) 3) Ręcznik i wodę 4) Rakietę (jeśli masz, często można wypożyczyć). To wystarczy! ",
            "Tak, buty są ważne! Potrzebujesz butów do sportów indoor z dobrą przyczepnością i stabilnością boczną. Unikaj butów do biegania - za mało stabilności.  Dobre opcje: buty do tenisa, squasha lub specjalne do padla.",
            "W squashu używa się małej, gumowej piłki z kropkami. Kropki oznaczają prędkość:  1 kropka (żółta) = najszybsza, 2 kropki (zielona/biała) = średnia.  Dla początkujących:  niebieska lub czerwona (wolniejsze, łatwiejsze do gry).",
            "Rakiety do padla:  Początkujący:  300-600 zł, Średniozaawansowani: 600-1200 zł, Profesjonalne: 1200-2000+ zł. Na start nie przepłacaj - 400-500 zł wystarczy na dobrą rakietę kontrolną.",
        ]
    },
    {
        "context": "Technika i poprawa gry",
        "questions": [
            "Jak poprawić swój backhand w squashu?",
            "Jakie są podstawowe uderzenia w padlu?",
            "Jak wykonać dobry serwis?",
            "Czym jest vibora w padlu?",
            "Jak trenować samemu?",
        ],
        "answers": [
            "Backhand w squashu: 1) Prawidłowy grip - continental 2) Rotacja bioder i ramion 3) Kontakt z piłką przed ciałem 4) Follow-through w kierunku celu.  Ćwicz przy ścianie solo, powtarzając ruch.  Filmuj się i analizuj.",
            "Podstawowe uderzenia w padlu: 1) Bandeja (defensywna smecz) 2) Vibora (ofensywna z rotacją) 3) Remate (smecz winner) 4) Chiquita (lob z returnu) 5) Bajada (volley przy siatce). Na start opanuj bandeję i podstawowe volleje.",
            "Dobry serwis w padlu: 1) Pozycja:  za linią serwisową 2) Piłka odbija się raz od podłoża 3) Uderzenie spodem/bokiem na wysokości pasa 4) Celuj w róg pola serwisowego 5) Obserwuj odbicie od ściany.  Trening:  powtarzaj 50x dziennie.",
            "Vibora to ofensywne uderzenie w padlu - połączenie między bandeją a rematem. Wykonujesz je z rotacją nadgarstka (slice), piłka ma backspin i po odbiciu zostaje nisko. Używane do ataku bez ryzyka auta.  Trudniejsze od bandei.",
            "Trening solo: 1) Padel/squash:  gra ze ścianą (volleje, returny) 2) Footwork: drabinka zwinności 3) Fizyka: sprint intervals, strength 4) Technika: nagrywaj się, analizuj 5) 15 min dziennie = widoczny progres w miesiąc! ",
        ]
    },
    {
        "context": "Różnice między sportami",
        "questions": [
            "Czym różni się padel od squasha? ",
            "Co jest trudniejsze - padel czy squash?",
            "Czy umiejętności z tenisa przydają się w padlu?",
            "Który sport jest lepszy dla początkujących?",
        ],
        "answers": [
            "Padel vs Squash:  PADEL - kort ze szkłem na zewnątrz, gra 2v2, rakieta solidna, wolniejsze tempo. SQUASH - zamknięty kort 4 ściany, głównie 1v1, rakieta ze strunami, bardzo szybkie tempo, bardziej fizyczne.",
            "To zależy!  Squash jest bardziej fizycznie wymagający (cardio, wytrzymałość), szybsze tempo.  Padel wymaga lepszej koordynacji zespołu (deblowa strategia) i czytania odbiać od szkła. Oba mają wysoki skill ceiling.  Padel łatwiejszy na start.",
            "Tak!  Z tenisa przeniesiesz:  techniki uderzeń (forehand/backhand), czucie piłki, footwork, taktykę debla. Musisz się przyzwyczaić do:  ścian w grze, niższego odbicia piłki, mniejszego kortu, innej rakiety.  Tenisiści szybko łapią padla! ",
            "PADEL łatwiejszy na start:  wolniejsza piłka, większa rakieta, gra zespołowa (partner pomaga), ściany dają więcej czasu.  SQUASH trudniejszy:  bardzo szybka piłka, mała rakieta, intensywne fizycznie.  Padel = bardziej social, Squash = bardziej workout.",
        ]
    },
]

SCENARIOS_EN = [
    {
        "context": "Rules and basics",
        "questions": [
            "What are the basic rules of padel?",
            "How do you play padel?",
            "What's the difference between padel and tennis?",
            "Can you use walls in padel?",
            "What does a padel court look like?",
        ],
        "answers": [
            "Padel is played 2v2 on a court surrounded by glass walls.  Serve underhand, ball must bounce in service box. You can use walls - ball can bounce off them!  Scoring like tennis: 15, 30, 40, game.",
            "Padel is played in doubles (2v2) on a smaller court than tennis. Court has glass walls you use during play. Serve underhand, scoring identical to tennis.",
            "Main differences: 1) Padel has glass walls you use in play 2) Smaller court 3) Always doubles (2v2) 4) Solid racket, no strings 5) Lower pressure ball.",
            "Yes! That's the main feature - you can bounce ball off glass walls. Ball must bounce on floor first, then can hit wall. You can also intentionally play into wall on your side.",
            "Padel court is 10x20m, surrounded by glass walls (3m high) and metal mesh.  Smaller than tennis court. Has net in middle and marked service boxes.",
        ]
    },
    {
        "context": "Finding partners",
        "questions": [
            "Looking for someone to play padel with",
            "How do I find a squash partner?",
            "Want to play tonight, anyone interested?",
            "I'm a beginner, looking for similar level",
        ],
        "answers": [
            "Great! I'll help you find a partner. Few questions: 1) What's your level (beginner/intermediate/advanced)? 2) What time?  3) Which area? 4) Have a court or need to book?",
            "I'll find squash partners for you! Tell me: your skill level, when you want to play, and location?  This helps match appropriate players.",
            "Excellent! To find partner for today: 1) Share your location 2) Preferred time 3) Skill level. I'll check who's available in your area!",
            "Perfect that you want similar level!  For beginners I recommend: 1) Local clubs 2) Beginner groups 3) Lessons with instructor to start. Want me to find beginners in your area? ",
        ]
    },
]

SYSTEM_PROMPTS = {
    'pl': "Jesteś pomocnym asystentem w aplikacji do łączenia graczy padla i squasha. Pomagasz użytkownikom znaleźć partnerów do gry, odpowiadasz na pytania o zasady, sprzęt i technikę.  Jesteś przyjazny, konkretny i zwięzły.",
    'en': "You are a helpful assistant in an app for matching community of padel and squash players. You help users find game partners, answer questions about rules, equipment and technique. You are friendly, specific and concise."
}


def generate_training_data(
    num_examples: int = 500,
    language: str = 'pl',
    seed: int = None
) -> List[Dict[str, Any]]:
    
    """
    Generates synthetic training data in ChatML format.
    
    Args:
        - num_examples: number of examples to generate
        - language: language code ('pl' or 'en')
        - seed: Random seed for reproducibility (optional)
    
    Returns:
        - list of dictionaries with messages key containing conversation
    """
    
    if seed:
        random.seed(seed)
    
    scenarios = SCENARIOS_PL if language == 'pl' else SCENARIOS_EN
    system_prompt = SYSTEM_PROMPTS[language]
    
    data = []
    
    for _ in range(num_examples):
        scenario = random.choice(scenarios)
        
        q_idx = random.randint(0, len(scenario['questions']) - 1)
        question = scenario['questions'][q_idx]
        answer = scenario['answers'][q_idx]
        
        example = {
            "messages": [
                {"role":  "system", "content": system_prompt},
                {"role": "user", "content": question},
                {"role": "assistant", "content": answer}
            ],
            "metadata": {
                "context": scenario["context"],
                "language": language,
                "generated_at": datetime.now().isoformat()
            }
        }
        
        data.append(example)
    
    return data
    
def save_dataset(
    data: List[Dict[str, Any]], 
    out_path: str | Path, 
    format: Literal['jsonl', 'json'] = 'jsonl'
) -> None:
    
    """
    Saves dataset to the output file. 
    
    Args:
        - data: list of synthetic training examples
        - out_path: output path file
        - format: output file format (default => 'jsonl')
    
    Returns:
        - None
    """

    output_path = Path(out_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            if format == 'jsonl': 
                for item in data:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
            elif format == 'json':
                json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                raise ValueError(f"Unsupported format: '{format}'. Use 'jsonl' or 'json'")
        
    except (IOError, OSError) as e:
        raise
    
def parse_args() -> None:
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        '-n', '--records',
        type=int,
        default=500,
        help='Number of training examples to generate (default: 500)'
    )
    
    parser.add_argument(
        '-l', '--language',
        choices=['pl', 'en'],
        default='pl',
        help='Data language: pl (Polish), en (English)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output file path (default: padel_train_{lang}.jsonl)'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['jsonl', 'json'],
        default='jsonl',
        help='Output format (default: jsonl)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Random seed for reproducibility (default: None)'
    )

def generate() -> None:
    args = parse_args()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    data = generate_training_data(
        args.records,
        args.language,
        args.seed
    )
    
    save_dataset(
        data, 
        output_dir, 
        args.format
    )


if __name__ == '__main__':
    generate()