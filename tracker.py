import streamlit as st
from datetime import date, timedelta
import json, os

st.set_page_config(page_title="DAILY OPS // ROUTINE TRACKER", page_icon="ðŸŽ¯",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Barlow+Condensed:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Barlow Condensed', sans-serif; background-color: #0d0e0b; color: #c8c9b8; }
.stApp { background-color: #0d0e0b; }
h1,h2,h3 { font-family: 'Share Tech Mono', monospace !important; color: #a8b86c !important; letter-spacing: 0.08em; }
.mission-header { font-family: 'Share Tech Mono', monospace; font-size: 2.1rem; color: #a8b86c; letter-spacing: 0.15em; border-bottom: 2px solid #a8b86c33; padding-bottom: 0.5rem; margin-bottom: 0.2rem; }
.subheader { font-family: 'Share Tech Mono', monospace; font-size: 0.85rem; color: #6b7c40; letter-spacing: 0.2em; margin-bottom: 1.5rem; }
.stat-box { background: #14160f; border: 1px solid #a8b86c33; border-left: 3px solid #a8b86c; padding: 1rem 1.2rem; border-radius: 2px; margin-bottom: 0.5rem; }
.stat-label { font-family: 'Share Tech Mono', monospace; font-size: 0.7rem; color: #6b7c40; letter-spacing: 0.2em; }
.stat-value { font-family: 'Share Tech Mono', monospace; font-size: 2rem; color: #a8b86c; font-weight: 700; }
.exercise-card { background: #14160f; border: 1px solid #2a2e1e; border-left: 4px solid #a8b86c; padding: 1rem 1.2rem; border-radius: 2px; margin-bottom: 10px; }
.exercise-name { font-family: 'Share Tech Mono', monospace; font-size: 1rem; color: #a8b86c; letter-spacing: 0.1em; margin-bottom: 4px; }
.exercise-desc { font-size: 0.95rem; color: #a8a99a; line-height: 1.5; margin-bottom: 8px; }
.exercise-tip { background: #1e2414; border-left: 2px solid #6b7c40; padding: 6px 10px; font-size: 0.85rem; color: #8a9a6c; border-radius: 0 2px 2px 0; margin-top: 6px; }
.muscle-badge { display: inline-block; background: #1e2414; border: 1px solid #a8b86c33; color: #a8b86c; font-family: 'Share Tech Mono', monospace; font-size: 0.6rem; letter-spacing: 0.1em; padding: 2px 8px; border-radius: 2px; margin-right: 4px; margin-bottom: 4px; }
.day-header { font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; color: #a8b86c; letter-spacing: 0.2em; background: #1a1e12; border: 1px solid #a8b86c33; padding: 8px 14px; border-radius: 2px; margin: 14px 0 8px; }
.rest-card { background: #0f110c; border: 1px solid #2a2e1e; border-left: 4px solid #3a4428; padding: 1rem 1.2rem; border-radius: 2px; color: #6b7c40; font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; letter-spacing: 0.1em; }
.divider { border: none; border-top: 1px solid #a8b86c22; margin: 1.5rem 0; }
.note-box { background: #14160f; border: 1px solid #a8b86c22; border-radius: 2px; padding: 0.8rem; font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; color: #8a9a5c; white-space: pre-wrap; }
[data-testid="stSidebar"] { background-color: #0a0c08 !important; border-right: 1px solid #a8b86c22; }
[data-testid="stSidebar"] * { color: #c8c9b8; }
.stCheckbox label { font-family: 'Barlow Condensed', sans-serif; font-size: 1rem; color: #c8c9b8; }
.stButton > button { font-family: 'Share Tech Mono', monospace; font-size: 0.75rem; letter-spacing: 0.12em; background: transparent; border: 1px solid #a8b86c66; color: #a8b86c; border-radius: 2px; padding: 0.4rem 1rem; }
.stButton > button:hover { background: #a8b86c22; border-color: #a8b86c; }
.stTextInput > div > div > input, .stTextArea textarea, .stSelectbox > div > div { background-color: #14160f !important; border: 1px solid #a8b86c33 !important; border-radius: 2px !important; color: #c8c9b8 !important; font-family: 'Barlow Condensed', sans-serif !important; }
.stProgress > div > div > div > div { background-color: #a8b86c !important; }
.stNumberInput > div > div > input { background-color: #14160f !important; border: 1px solid #a8b86c33 !important; color: #a8b86c !important; font-family: 'Share Tech Mono', monospace !important; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# â”€â”€ Constants â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
DATA_FILE   = "routine_data.json"
today_str   = str(date.today())
today_label = date.today().strftime("%A").upper()

DEFAULT_TASKS = [
    {"id":"t01","name":"WAKE UP + FRESHEN UP",      "time":"05:00",         "session":"MORNING",   "category":"Health",  "day":"All"},
    {"id":"t02","name":"RUNNING",                   "time":"05:30 â€“ 06:00", "session":"MORNING",   "category":"Health",  "day":"All"},
    {"id":"t03","name":"CALISTHENICS",              "time":"06:00 â€“ 07:00", "session":"MORNING",   "category":"Health",  "day":"All"},
    {"id":"t04","name":"COOLDOWN & SHOWER",         "time":"07:00 â€“ 07:30", "session":"MORNING",   "category":"Health",  "day":"All"},
    {"id":"t05","name":"BREAKFAST",                 "time":"07:30 â€“ 08:00", "session":"MORNING",   "category":"Health",  "day":"All"},
    {"id":"t06","name":"STUDY â€” MATHS",             "time":"08:00 â€“ 10:00", "session":"MORNING",   "category":"Study",   "day":"Monday,Thursday"},
    {"id":"t07","name":"STUDY â€” PHYSICS",           "time":"08:00 â€“ 10:00", "session":"MORNING",   "category":"Study",   "day":"Tuesday,Friday"},
    {"id":"t08","name":"STUDY â€” CHEMISTRY",         "time":"08:00 â€“ 10:00", "session":"MORNING",   "category":"Study",   "day":"Wednesday,Saturday"},
    {"id":"t09","name":"PYTHON â€” BASIC CONCEPTS",  "time":"13:00 â€“ 15:00", "session":"AFTERNOON", "category":"Python",  "day":"All"},
    {"id":"t10","name":"PYTHON â€” PRACTICE PROBLEM","time":"13:00 â€“ 15:00", "session":"AFTERNOON", "category":"Python",  "day":"All"},
    {"id":"t11","name":"AI â€” PROMPT ENGINEERING",  "time":"16:00 â€“ 17:00", "session":"AFTERNOON", "category":"AI",      "day":"All"},
    {"id":"t12","name":"READING â€” SELF IMPROVEMENT","time":"17:30 â€“ 19:00","session":"AFTERNOON", "category":"Personal","day":"All"},
    {"id":"t13","name":"REVISE + KEY POINTS",       "time":"19:30 â€“ 20:30", "session":"EVENING",   "category":"Study",   "day":"All"},
    {"id":"t14","name":"SLEEP",                     "time":"23:00",         "session":"NIGHT",     "category":"Health",  "day":"All"},
]

WORKOUT_PLAN = {
    "Monday": {
        "focus": "PUSH â€” CHEST / SHOULDERS / TRICEPS",
        "exercises": [
            {"id":"w_mon_01","name":"STANDARD PUSH-UPS",
             "muscles":["Chest","Triceps","Front Delts"],
             "description":"Your base. 100 reps (5Ã—20) is where you start â€” but here we push beyond that with heavier variations to keep growing.",
             "how_to":"Hands shoulder-width, body rigid from head to heel. Lower chest to 1 inch off floor, lock out at top. No sagging hips, no half reps.",
             "tip":"Squeeze glutes and core the entire set â€” this makes every rep 30% harder and protects your lower back.",
             "default_sets":5,"default_reps":20},
            {"id":"w_mon_02","name":"WIDE PUSH-UPS",
             "muscles":["Outer Chest","Front Delts"],
             "description":"Hands 6â€“8 inches wider than shoulders. Hits the outer chest and gives you that broad, full pec look.",
             "how_to":"Wide hand placement, elbows flare 45â€“60Â°. Lower until chest nearly touches. Squeeze chest at top of each rep.",
             "tip":"Don't let elbows go past 90Â° â€” keep tension on the chest, not the shoulder joints.",
             "default_sets":4,"default_reps":15},
            {"id":"w_mon_03","name":"DIAMOND PUSH-UPS",
             "muscles":["Triceps","Inner Chest"],
             "description":"Hands form a diamond under your chest. One of the hardest push-up variations â€” builds horseshoe triceps fast.",
             "how_to":"Index fingers and thumbs touching in a diamond shape. Keep elbows tight to body as you lower. Full range every rep.",
             "tip":"If too hard initially, elevate hands on a chair. Progress to floor level within 2 weeks.",
             "default_sets":4,"default_reps":12},
            {"id":"w_mon_04","name":"PIKE PUSH-UPS",
             "muscles":["Shoulders","Upper Chest","Triceps"],
             "description":"Inverted V position. Your gateway to the handstand push-up â€” directly trains overhead pressing strength.",
             "how_to":"Downward dog position. Keeping hips high, bend elbows and lower head toward floor between your hands. Press back up.",
             "tip":"Closer feet = harder. Progress by elevating feet on a chair to mimic a wall handstand push-up.",
             "default_sets":4,"default_reps":10},
            {"id":"w_mon_05","name":"TRICEP DIPS (CHAIR)",
             "muscles":["Triceps","Lower Chest","Front Delts"],
             "description":"Use any stable chair. Directly isolates the tricep â€” crucial for locking out every pushing movement.",
             "how_to":"Hands on chair edge behind you, legs extended. Lower until upper arms parallel to floor. Press back up. Back stays close to chair.",
             "tip":"Bend knees to reduce difficulty. Elevate feet to increase it. Slow negatives (3 sec down) for maximum growth.",
             "default_sets":4,"default_reps":15},
        ]
    },
    "Tuesday": {
        "focus": "PULL â€” BACK / BICEPS",
        "exercises": [
            {"id":"w_tue_01","name":"PULL-UPS (OVERHAND)",
             "muscles":["Lats","Upper Back","Biceps"],
             "description":"The king of upper body pulling. Overhand grip builds the wide, thick lats that create the V-taper physique.",
             "how_to":"Dead hang, overhand grip shoulder-width or wider. Pull until chin clears bar. Lower SLOWLY â€” 3 seconds down. Zero kipping.",
             "tip":"The negative (lowering) phase builds as much muscle as the pull. Never drop fast from the top.",
             "default_sets":5,"default_reps":8},
            {"id":"w_tue_02","name":"CHIN-UPS (UNDERHAND)",
             "muscles":["Biceps","Lower Lats","Chest"],
             "description":"Underhand grip activates your biceps maximally. You'll be able to do more reps than overhand â€” use that advantage.",
             "how_to":"Underhand shoulder-width grip. Pull driving elbows down and back. Squeeze biceps hard at top. Full hang at bottom each rep.",
             "tip":"Rotate your wrists inward as you pull â€” this supination is what maximally fires the bicep peak.",
             "default_sets":4,"default_reps":10},
            {"id":"w_tue_03","name":"INVERTED ROWS (UNDER TABLE)",
             "muscles":["Mid Back","Rhomboids","Rear Delts","Biceps"],
             "description":"Lie under a sturdy table, grab the edge, pull chest up. Horizontal pulling â€” the exercise that fixes rounded shoulders.",
             "how_to":"Body straight, heels on floor under table. Pull chest to table, squeeze shoulder blades together at top. Lower slowly.",
             "tip":"Elevate feet on chair to increase difficulty. This directly counters the forward posture caused by desk work and phones.",
             "default_sets":4,"default_reps":12},
            {"id":"w_tue_04","name":"SCAPULAR PULL-UPS",
             "muscles":["Serratus","Lower Traps","Lats"],
             "description":"Hang, then depress shoulder blades WITHOUT bending elbows. Tiny movement, enormous benefit. Unlocks muscle control most people never develop.",
             "how_to":"Dead hang. Without bending arms, pull shoulder blades DOWN and BACK â€” body rises slightly. Hold 1 second at top. Release slowly.",
             "tip":"This protects your shoulder joint and is mandatory for front lever and muscle-up progressions.",
             "default_sets":3,"default_reps":10},
            {"id":"w_tue_05","name":"DEAD HANGS",
             "muscles":["Grip Strength","Lats","Shoulder Health"],
             "description":"Hang from bar for time. Builds iron grip, decompresses spine, develops the shoulder stability needed for every advanced skill.",
             "how_to":"Full arm extension hang. Relax legs, breathe deep. Hold for 30â€“60 seconds. Alternate grip each set.",
             "tip":"Grip strength is your limiting factor in ALL pulling work. Train it seriously every session.",
             "default_sets":3,"default_reps":45},
        ]
    },
    "Wednesday": {
        "focus": "LEGS â€” QUADS / HAMSTRINGS / GLUTES / CALVES",
        "exercises": [
            {"id":"w_wed_01","name":"BODYWEIGHT SQUATS",
             "muscles":["Quads","Glutes","Hamstrings"],
             "description":"Foundation of all leg training. High volume builds endurance, strength, and leg mass with zero equipment.",
             "how_to":"Feet shoulder-width, toes slightly out. Sit back and down to parallel. Drive through heels to stand. Chest tall, knees track over toes.",
             "tip":"2-second pause at the bottom eliminates momentum and forces muscles to do all the work.",
             "default_sets":5,"default_reps":25},
            {"id":"w_wed_02","name":"JUMP SQUATS",
             "muscles":["Quads","Glutes","Calves","Explosiveness"],
             "description":"Squat down, explode up as high as possible. Builds fast-twitch muscle and raw athletic power â€” separates athletes from gym-goers.",
             "how_to":"Squat to parallel, drive through floor explosively and jump. Land softly with bent knees, absorb impact, flow into next rep.",
             "tip":"Land quietly. Noisy landings mean bad mechanics and joint stress. Quiet = controlled = safe.",
             "default_sets":4,"default_reps":15},
            {"id":"w_wed_03","name":"REVERSE LUNGES",
             "muscles":["Quads","Glutes","Hamstrings","Balance"],
             "description":"Step backward instead of forward â€” far less knee stress than forward lunges. Builds single-leg strength and balance.",
             "how_to":"Stand tall, step one foot back. Lower back knee toward floor. Front thigh parallel to floor. Push through front heel to return.",
             "tip":"Keep torso completely upright. Leaning forward shifts the load from glutes to lower back â€” a common and painful mistake.",
             "default_sets":4,"default_reps":12},
            {"id":"w_wed_04","name":"GLUTE BRIDGES",
             "muscles":["Glutes","Hamstrings","Lower Back"],
             "description":"Lie on back, drive hips to ceiling. Most people have chronically weak glutes from sitting â€” this fixes that directly.",
             "how_to":"Lie on back, knees bent, feet flat. Drive hips up until body is a straight line from knees to shoulders. Squeeze glutes at top for 2 seconds.",
             "tip":"Press lower back flat before lifting. Progress to single-leg version â€” one of the best glute exercises in existence.",
             "default_sets":4,"default_reps":20},
            {"id":"w_wed_05","name":"CALF RAISES",
             "muscles":["Gastrocnemius","Soleus"],
             "description":"Rise up on toes, lower slowly. Calves handle all your walking load daily, so they need high reps and slow negatives to grow.",
             "how_to":"Stand on edge of step. Rise as high as possible on toes. Lower SLOWLY over 3 full seconds all the way down. Full range every rep.",
             "tip":"The slow negative is what makes calves grow â€” they are notoriously stubborn for a reason. Go full range, go slow.",
             "default_sets":4,"default_reps":25},
        ]
    },
    "Thursday": {
        "focus": "CORE â€” ABS / OBLIQUES / LOWER BACK",
        "exercises": [
            {"id":"w_thu_01","name":"PLANK (SECONDS)",
             "muscles":["Core","Transverse Abs","Shoulders"],
             "description":"The best core exercise period. Builds anti-rotation and anti-extension strength â€” the foundation of every advanced calisthenics skill.",
             "how_to":"Forearms on floor, elbows under shoulders. Body straight head to heel. Squeeze glutes, abs, and quads. Breathe slowly through nose.",
             "tip":"Think 'pull elbows toward feet' â€” this activates lats and makes the plank significantly harder.",
             "default_sets":4,"default_reps":60},
            {"id":"w_thu_02","name":"HOLLOW BODY HOLD (SECONDS)",
             "muscles":["Abs","Hip Flexors","Core Stability"],
             "description":"The gymnastics core position. Required for front lever, handstand, and muscle-up. Looks simple, is brutal.",
             "how_to":"Lie on back. Press lower back INTO floor (non-negotiable). Lift legs to 30Â°, arms overhead, shoulders off ground. Hold.",
             "tip":"If lower back lifts off the floor, raise your legs until it stays flat. Never sacrifice form for lower legs.",
             "default_sets":4,"default_reps":30},
            {"id":"w_thu_03","name":"BICYCLE CRUNCHES",
             "muscles":["Obliques","Rectus Abs","Hip Flexors"],
             "description":"The highest EMG-rated ab exercise for obliques. The twisting motion is what builds the side definition most people chase.",
             "how_to":"Hands lightly behind head. Lift shoulders. Bring right elbow to left knee while extending right leg. Alternate slowly.",
             "tip":"Slow down by 50%. Fast bicycle crunches just swing elbows â€” slow ones actually build obliques.",
             "default_sets":3,"default_reps":20},
            {"id":"w_thu_04","name":"LEG RAISES",
             "muscles":["Lower Abs","Hip Flexors"],
             "description":"Raise straight legs from floor to vertical. Directly hits lower abs â€” the hardest area to develop and the last to show.",
             "how_to":"Lie flat, hands under lower back. Legs straight, raise to 90Â°. Lower slowly over 3 seconds. Feet never touch floor between reps.",
             "tip":"The moment your lower back arches, you lose core engagement and gain injury risk. Keep it pressed flat always.",
             "default_sets":4,"default_reps":15},
            {"id":"w_thu_05","name":"SUPERMAN HOLDS",
             "muscles":["Lower Back","Glutes","Rear Delts"],
             "description":"Lie face down, lift arms and legs simultaneously. Directly strengthens the lower back â€” your most injury-vulnerable area.",
             "how_to":"Face down, arms extended overhead. Simultaneously lift arms, chest, and legs. Hold 2 seconds at top. Lower slowly.",
             "tip":"Squeeze glutes hard at the top â€” this reduces shear force on lumbar vertebrae and protects your spine.",
             "default_sets":3,"default_reps":12},
        ]
    },
    "Friday": {
        "focus": "PUSH SKILLS â€” ADVANCED PROGRESSIONS",
        "exercises": [
            {"id":"w_fri_01","name":"ARCHER PUSH-UPS",
             "muscles":["Chest","Triceps","Shoulders"],
             "description":"One arm does most of the work, the other extends sideways. This is your direct progression toward the one-arm push-up.",
             "how_to":"Wide stance. As you lower, shift weight to one arm while the other extends straight to the side. Alternate each rep.",
             "tip":"Gradually try to peel the extended arm off the ground as you get stronger. That moment is the one-arm push-up.",
             "default_sets":4,"default_reps":8},
            {"id":"w_fri_02","name":"DECLINE PUSH-UPS",
             "muscles":["Upper Chest","Front Delts","Triceps"],
             "description":"Feet elevated on chair â€” targets the upper chest. The higher the elevation, the more it becomes a shoulder exercise.",
             "how_to":"Feet on chair (45cm+). Hands shoulder-width. Lower chest to floor. Core tight. Drive back up through full lockout.",
             "tip":"Progress by using a higher surface. Wall push-ups are the hardest (near-vertical) â€” that's your long-term goal here.",
             "default_sets":4,"default_reps":15},
            {"id":"w_fri_03","name":"PUSH-UP BOTTOM HOLD (SECONDS)",
             "muscles":["Chest","Triceps","Core"],
             "description":"Hold the bottom position of a push-up. Isometric training at the hardest point. 10 seconds here outperforms 10 fast reps.",
             "how_to":"Lower to 1 inch off floor. Hold. Body perfectly rigid â€” no sagging, no shaking the reps off. Pure stillness.",
             "tip":"This is brutal and humbling. It is also the fastest way to break through push-up plateaus.",
             "default_sets":3,"default_reps":20},
            {"id":"w_fri_04","name":"MOUNTAIN CLIMBERS",
             "muscles":["Core","Hip Flexors","Shoulders","Cardio"],
             "description":"Alternating knee drives in push-up position. Builds core endurance and conditioning simultaneously â€” a 2-in-1 weapon.",
             "how_to":"Push-up position. Drive one knee toward chest, alternate rapidly. Hips stay level â€” they must not rise or sag.",
             "tip":"Slow = core drill. Fast = cardio drill. Both are valid depending on your goal for the set.",
             "default_sets":4,"default_reps":30},
            {"id":"w_fri_05","name":"HANDSTAND WALL HOLD (SECONDS)",
             "muscles":["Shoulders","Core","Balance","Wrists"],
             "description":"Kick up to a wall handstand and hold. The path to a freestanding handstand â€” one of the ultimate calisthenics skills.",
             "how_to":"Face wall, hands close. Kick up one leg then the other. Chest faces wall. Press the floor away. Hold and breathe.",
             "tip":"Point toes, squeeze glutes, push floor away with straight arms. Think about lifting your hips directly above your hands.",
             "default_sets":3,"default_reps":20},
        ]
    },
    "Saturday": {
        "focus": "FULL BODY â€” POWER + ENDURANCE",
        "exercises": [
            {"id":"w_sat_01","name":"BURPEES",
             "muscles":["Full Body","Cardio","Explosiveness"],
             "description":"The ultimate conditioning exercise. Combines squat, push-up, and jump. Used by every serious military programme worldwide.",
             "how_to":"Stand â†’ squat â†’ jump feet back â†’ push-up â†’ jump feet forward â†’ jump up with arms overhead. Full push-up every time.",
             "tip":"The push-up is non-negotiable. Skipping it means you are not doing burpees â€” you are doing something easier.",
             "default_sets":5,"default_reps":10},
            {"id":"w_sat_02","name":"PULL-UP + PUSH-UP SUPERSET",
             "muscles":["Full Upper Body"],
             "description":"Pull-ups followed immediately by push-ups with no rest between. Classic military superset for balanced upper body strength.",
             "how_to":"5 pull-ups â†’ immediately 10 push-ups â†’ rest 60 seconds. That is one set. Ratio is always 1:2 (pull:push).",
             "tip":"Your pushing muscles rest while your pulling muscles work â€” zero downtime. This is efficient training.",
             "default_sets":5,"default_reps":5},
            {"id":"w_sat_03","name":"JUMP SQUAT + PUSH-UP CIRCUIT",
             "muscles":["Legs","Chest","Cardio"],
             "description":"10 jump squats then 10 push-ups, repeat. This circuit trains your entire body and your conditioning simultaneously.",
             "how_to":"10 jump squats (max height) â†’ drop to floor â†’ 10 push-ups â†’ stand â†’ repeat. Rest 90 seconds between full rounds.",
             "tip":"Pace yourself on round 1. The cumulative fatigue is severe by round 3.",
             "default_sets":4,"default_reps":10},
            {"id":"w_sat_04","name":"TUCK HOLD â€” BAR OR FLOOR (SECONDS)",
             "muscles":["Core","Hip Flexors","Lats"],
             "description":"Hang from bar, pull knees to chest and hold. Floor version: L-sit progression on chairs. Your path to the front lever.",
             "how_to":"Hang from bar. Pull knees to chest tight, hold as long as possible. Floor: support on two chairs, lift knees to chest.",
             "tip":"Push the bar DOWN as you hold â€” lat activation makes the position dramatically stronger.",
             "default_sets":3,"default_reps":20},
            {"id":"w_sat_05","name":"100 PUSH-UP FINISHER",
             "muscles":["Chest","Triceps","Mental Toughness"],
             "description":"100 push-ups any way you can. This is your signature. End every Saturday by owning it. Your benchmark is 5Ã—20.",
             "how_to":"5Ã—20 is your standard split. As you grow: try 4Ã—25, then 2Ã—50, then 100 unbroken. Track your split each week.",
             "tip":"Track set breakdown weekly. The goal is fewer sets, faster. That progress IS your strength gain.",
             "default_sets":5,"default_reps":20},
        ]
    },
    "Sunday": {
        "focus": "REST + ACTIVE RECOVERY",
        "exercises": [
            {"id":"w_sun_01","name":"DEEP STRETCHING â€” FULL BODY",
             "muscles":["Flexibility","Recovery"],
             "description":"Hold each position 60+ seconds. Flexibility is trainable. Neglecting it shortens your athletic lifespan dramatically.",
             "how_to":"Target: hip flexors (lunge), hamstrings (forward fold), chest (doorway), shoulders (cross-body), thoracic spine (thread needle).",
             "tip":"Breathe into each stretch. On every exhale, consciously release deeper. Never force or bounce.",
             "default_sets":1,"default_reps":10},
            {"id":"w_sun_02","name":"LIGHT WALKING (MINUTES)",
             "muscles":["Active Recovery","Blood Flow"],
             "description":"20â€“30 minutes at easy pace. Increases blood flow to sore muscles, accelerates recovery without adding training stress.",
             "how_to":"Comfortable pace, nose breathing. This is a mental reset as much as physical. No running, no rushing.",
             "tip":"Walk barefoot on grass where possible â€” research shows grounding reduces systemic inflammation markers.",
             "default_sets":1,"default_reps":25},
            {"id":"w_sun_03","name":"JOINT MOBILITY CIRCLES",
             "muscles":["Joints","Injury Prevention","Longevity"],
             "description":"Circle every major joint through full range. This 10-minute practice prevents injuries and adds years of pain-free training.",
             "how_to":"10 slow circles each direction: wrists, elbows, shoulders, neck, thoracic spine, hips, knees, ankles.",
             "tip":"This routine done consistently on rest days is worth more than any supplement you could buy.",
             "default_sets":1,"default_reps":10},
        ]
    },
}

# â”€â”€ Data helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"tasks": DEFAULT_TASKS, "history": {}, "notes": {}, "workout_reps": {}}

def save_data(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, indent=2)

data = load_data()
if not data.get("tasks"):       data["tasks"] = DEFAULT_TASKS
if "workout_reps" not in data:  data["workout_reps"] = {}
save_data(data)

def get_today_tasks():
    return [t for t in data["tasks"]
            if t.get("day","All") == "All" or today_label in t.get("day","").upper()]

def calc_streak():
    streak, check = 0, date.today() - timedelta(days=1)
    for _ in range(60):
        ds = str(check)
        hist = data["history"].get(ds, [])
        day_tasks = [t for t in data["tasks"]
                     if t.get("day","All") == "All"
                     or check.strftime("%A").upper() in t.get("day","").upper()]
        if day_tasks and len(hist) >= len(day_tasks):
            streak += 1; check -= timedelta(days=1)
        else:
            break
    return streak

def get_w(eid, field, default):
    return data["workout_reps"].get(f"{eid}_{field}", default)

def set_w(eid, field, val):
    data["workout_reps"][f"{eid}_{field}"] = val

# â”€â”€ Layout â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown('<div class="mission-header">// DAILY OPS TRACKER</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subheader">OPERATIVE: ACTIVE DUTY &nbsp;|&nbsp; DATE: {date.today().strftime("%d %b %Y").upper()} &nbsp;|&nbsp; {today_label}</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### // MISSION CONTROL")
    tab = st.radio("Nav", ["TODAY","WORKOUT","HISTORY","EDIT TASKS","NOTES"], label_visibility="collapsed")

# â•â•â•â•â•â•â•â•â•â•â•â• TODAY â•â•â•â•â•â•â•â•â•â•â•â•
if tab == "TODAY":
    today_tasks = get_today_tasks()
    if today_str not in data["history"]: data["history"][today_str] = []
    completed = data["history"][today_str]
    streak = calc_streak()
    total = len(today_tasks)
    done  = len([t for t in today_tasks if t["id"] in completed])
    pct   = int(done/total*100) if total else 0

    c1,c2,c3,c4 = st.columns(4)
    for col, lbl, val in [(c1,"TASKS TODAY",total),(c2,"COMPLETED",done),(c3,"COMPLETION",f"{pct}%"),(c4,"STREAK",f"ðŸ”¥{streak}d")]:
        with col:
            st.markdown(f'<div class="stat-box"><div class="stat-label">{lbl}</div><div class="stat-value">{val}</div></div>', unsafe_allow_html=True)
    st.progress(pct/100)
    if pct==100: st.success("âš¡ ALL OBJECTIVES COMPLETE. MISSION SUCCESS.")
    elif pct>=70: st.info("ðŸ’ª STRONG PROGRESS â€” MAINTAIN DISCIPLINE.")
    elif pct>=40: st.warning("âš ï¸ HALFWAY â€” PUSH HARDER, SOLDIER.")
    else: st.error("ðŸŽ¯ MISSION IN PROGRESS â€” ZERO EXCUSES.")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    for session in ["MORNING","AFTERNOON","EVENING","NIGHT"]:
        s_tasks = [t for t in today_tasks if t.get("session")==session]
        if not s_tasks: continue
        st.markdown(f"**[ {session} ]**")
        for task in s_tasks:
            tid = task["id"]
            checked = st.checkbox(f"**{task['name']}** â€” `{task['time']}`  _{task['category']}_",
                                   value=tid in completed, key=f"chk_{tid}_{today_str}")
            if checked and tid not in completed:
                completed.append(tid); save_data(data); st.rerun()
            elif not checked and tid in completed:
                completed.remove(tid); save_data(data); st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("**// FIELD NOTES**")
    existing = data.get("notes",{}).get(today_str,"")
    note = st.text_area("Log today's wins, struggles...", value=existing, height=100, label_visibility="collapsed")
    if st.button("ðŸ’¾ SAVE NOTE"):
        if "notes" not in data: data["notes"] = {}
        data["notes"][today_str] = note; save_data(data); st.success("Note saved.")

# â•â•â•â•â•â•â•â•â•â•â•â• WORKOUT â•â•â•â•â•â•â•â•â•â•â•â•
elif tab == "WORKOUT":
    st.markdown("### // CALISTHENICS BATTLE PLAN")
    st.markdown("6-day progressive plan built around your 100 push-up base. Edit any sets/reps â€” saved permanently.")

    days_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    current_day = date.today().strftime("%A")
    default_idx = days_order.index(current_day) if current_day in days_order else 0
    selected = st.selectbox("Select training day", days_order, index=default_idx, label_visibility="collapsed")

    plan = WORKOUT_PLAN[selected]
    st.markdown(f'<div class="day-header">[ {selected.upper()} ] â€” {plan["focus"]}</div>', unsafe_allow_html=True)

    if selected == "Sunday":
        st.markdown('<div class="rest-card">// REST DAY â€” ACTIVE RECOVERY ONLY<br>Growth happens during rest. Protect this day.</div>', unsafe_allow_html=True)
        st.markdown("")

    TIME_FIELDS = {"w_thu_01","w_thu_02","w_fri_03","w_fri_05","w_sat_04","w_tue_05"}

    for ex in plan["exercises"]:
        eid = ex["id"]
        saved_sets = int(get_w(eid,"sets",ex["default_sets"]))
        saved_reps = int(get_w(eid,"reps",ex["default_reps"]))
        unit = "SEC" if eid in TIME_FIELDS else "MIN" if "WALKING" in ex["name"] else "REPS"

        badges = "".join([f'<span class="muscle-badge">{m.upper()}</span>' for m in ex["muscles"]])
        st.markdown(f"""
<div class="exercise-card">
  <div class="exercise-name">{ex["name"]}</div>
  <div style="margin-bottom:8px;">{badges}</div>
  <div class="exercise-desc">{ex["description"]}</div>
  <div class="exercise-tip">â–¶ HOW TO PERFORM: {ex["how_to"]}</div>
  <div class="exercise-tip" style="margin-top:4px; border-left-color:#a8b86c;">âš¡ OPERATOR TIP: {ex["tip"]}</div>
</div>""", unsafe_allow_html=True)

        cs, cr, cb = st.columns([1,1,1])
        with cs:
            new_sets = st.number_input("SETS", min_value=1, max_value=20, value=saved_sets, key=f"s_{eid}", step=1)
        with cr:
            new_reps = st.number_input(unit, min_value=1, max_value=300, value=saved_reps, key=f"r_{eid}", step=1)
        with cb:
            st.markdown("<div style='margin-top:28px;'>", unsafe_allow_html=True)
            if st.button("ðŸ’¾ SAVE", key=f"bw_{eid}"):
                set_w(eid,"sets",new_sets); set_w(eid,"reps",new_reps)
                save_data(data); st.success(f"Saved: {new_sets} Ã— {new_reps} {unit}")
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("")

    # Weekly overview strip
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("**// WEEKLY SPLIT OVERVIEW**")
    cols = st.columns(7)
    for i, d in enumerate(days_order):
        focus_short = WORKOUT_PLAN[d]["focus"].split("â€”")[0].strip()
        is_today = d == current_day
        border = "border:2px solid #a8b86c;" if is_today else "border:1px solid #2a2e1e;"
        with cols[i]:
            st.markdown(
                f'<div style="background:#14160f;{border}border-radius:2px;padding:8px 4px;text-align:center;">'
                f'<div style="font-family:Share Tech Mono,monospace;font-size:0.6rem;color:#a8b86c;">{d[:3].upper()}</div>'
                f'<div style="font-size:0.6rem;color:#6b7c40;margin-top:4px;line-height:1.3;">{focus_short}</div>'
                f'</div>', unsafe_allow_html=True)

# â•â•â•â•â•â•â•â•â•â•â•â• HISTORY â•â•â•â•â•â•â•â•â•â•â•â•
elif tab == "HISTORY":
    st.markdown("### // MISSION HISTORY")
    try:
        import plotly.graph_objects as go
        HAS_PLOTLY = True
    except ImportError:
        HAS_PLOTLY = False
        st.warning("Run `pip install plotly` for the performance graph.")

    dates, percents = [], []
    for i in range(13, -1, -1):
        d = date.today() - timedelta(days=i)
        ds = str(d); dn = d.strftime("%A").upper()
        day_tasks = [t for t in data["tasks"] if t.get("day","All")=="All" or dn in t.get("day","").upper()]
        hist = data["history"].get(ds, [])
        total = len(day_tasks)
        done  = len([h for h in hist if h in [t["id"] for t in day_tasks]])
        pct   = int(done/total*100) if total else 0
        dates.append(d.strftime("%d %b")); percents.append(pct)

    if HAS_PLOTLY:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=dates, y=percents,
            marker_color=["#a8b86c" if p==100 else "#4a5c28" if p>=50 else "#2a3018" for p in percents], name="Completion %"))
        fig.add_trace(go.Scatter(x=dates, y=percents, mode="lines+markers",
            line=dict(color="#c8d88c",width=2), marker=dict(color="#a8b86c",size=6), name="Trend"))
        fig.update_layout(paper_bgcolor="#0d0e0b", plot_bgcolor="#0d0e0b",
            font=dict(family="Share Tech Mono, monospace", color="#a8b86c"),
            title=dict(text="// 14-DAY PERFORMANCE LOG", font=dict(size=14,color="#a8b86c")),
            yaxis=dict(range=[0,100], ticksuffix="%", gridcolor="#1e2414", color="#6b7c40"),
            xaxis=dict(gridcolor="#1e2414", color="#6b7c40"),
            legend=dict(bgcolor="#0d0e0b", bordercolor="#a8b86c33"),
            margin=dict(l=10,r=10,t=50,b=10), height=340)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart({"Completion %": percents}, height=250)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("**// DAILY LOGS**")
    past = sorted([d for d in data["history"].keys() if d!=today_str], reverse=True)
    for ds in past[:10]:
        d = date.fromisoformat(ds); dn = d.strftime("%A").upper()
        day_tasks = [t for t in data["tasks"] if t.get("day","All")=="All" or dn in t.get("day","").upper()]
        hist = data["history"].get(ds,[])
        done = len([h for h in hist if h in [t["id"] for t in day_tasks]])
        total= len(day_tasks); pct = int(done/total*100) if total else 0
        note = data.get("notes",{}).get(ds,"")
        with st.expander(f"{d.strftime('%A %d %b %Y').upper()}  â€”  {done}/{total}  ({pct}%)"):
            st.progress(pct/100)
            for t in day_tasks:
                st.markdown(f"{'âœ…' if t['id'] in hist else 'âŒ'} {t['name']}")
            if note:
                st.markdown(f'<div class="note-box">ðŸ“ {note}</div>', unsafe_allow_html=True)

# â•â•â•â•â•â•â•â•â•â•â•â• EDIT TASKS â•â•â•â•â•â•â•â•â•â•â•â•
elif tab == "EDIT TASKS":
    st.markdown("### // EDIT MISSION TASKS")
    with st.expander("âž• ADD NEW TASK", expanded=False):
        n_name = st.text_input("Task name", placeholder="e.g. MEDITATION")
        n_time = st.text_input("Time", placeholder="e.g. 06:00 â€“ 06:30")
        n_sess = st.selectbox("Session", ["MORNING","AFTERNOON","EVENING","NIGHT"])
        n_cat  = st.selectbox("Category", ["Health","Study","Python","AI","Personal","Other"])
        n_day  = st.selectbox("Days", ["All","Monday,Thursday","Tuesday,Friday","Wednesday,Saturday",
                                        "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        if st.button("ADD TASK"):
            if n_name.strip():
                data["tasks"].append({"id":f"t{len(data['tasks'])+1:02d}_{today_str}",
                    "name":n_name.strip().upper(),"time":n_time,"session":n_sess,"category":n_cat,"day":n_day})
                save_data(data); st.success("Task added."); st.rerun()
            else: st.error("Enter a task name.")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("**// CURRENT TASKS**")
    cats = ["Health","Study","Python","AI","Personal","Other"]
    for i, task in enumerate(data["tasks"]):
        with st.expander(f"[{task['session']}] {task['name']} â€” {task['time']}"):
            e_name = st.text_input("Name", value=task["name"], key=f"en_{i}")
            e_time = st.text_input("Time", value=task["time"], key=f"et_{i}")
            e_sess = st.selectbox("Session", ["MORNING","AFTERNOON","EVENING","NIGHT"],
                index=["MORNING","AFTERNOON","EVENING","NIGHT"].index(task.get("session","MORNING")), key=f"es_{i}")
            e_cat  = st.selectbox("Category", cats,
                index=cats.index(task.get("category","Health")) if task.get("category") in cats else 0, key=f"ec_{i}")
            e_day  = st.text_input("Days", value=task.get("day","All"), key=f"ed_{i}")
            cs2, cd2 = st.columns(2)
            with cs2:
                if st.button("ðŸ’¾ SAVE", key=f"save_{i}"):
                    data["tasks"][i].update({"name":e_name.upper(),"time":e_time,"session":e_sess,"category":e_cat,"day":e_day})
                    save_data(data); st.success("Saved."); st.rerun()
            with cd2:
                if st.button("ðŸ—‘ DELETE", key=f"del_{i}"):
                    data["tasks"].pop(i); save_data(data); st.rerun()

# â•â•â•â•â•â•â•â•â•â•â•â• NOTES â•â•â•â•â•â•â•â•â•â•â•â•
elif tab == "NOTES":
    st.markdown("### // FIELD NOTES LOG")
    all_noted = sorted([d for d in data.get("notes",{}).keys() if data["notes"][d].strip()], reverse=True)
    if not all_noted:
        st.info("No notes yet. Add them from the TODAY view.")
    for ds in all_noted:
        d = date.fromisoformat(ds)
        st.markdown(f"**{d.strftime('%A %d %b %Y').upper()}**")
        st.markdown(f'<div class="note-box">{data["notes"][ds]}</div>', unsafe_allow_html=True)
        st.markdown("")
