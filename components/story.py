import streamlit as st
import io
from gtts import gTTS
from dotenv import load_dotenv
import os
import re
import google.generativeai as genai
# --- MODIFICATION: Import Hugging Face client ---
#from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

# Get Google API Key from Streamlit secrets
google_api_key = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))

if not google_api_key:
    st.error("❌ GOOGLE_API_KEY is not set.")
    st.stop()

# Configure the generative AI model
try:
    genai.configure(api_key=google_api_key)
    # Using gemini-1.5-flash as it's fast and effective for creative text
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 
except Exception as e:
    st.error(f"Could not initialize the Google Generative AI Client. Error: {e}")
    st.stop()



# --- Main Render Function ---
def render(go_to_next_page):
    # This is a guard clause. To see this page, you MUST navigate from the previous pages.
    if "sc_scores" not in st.session_state or "personal_data" not in st.session_state:
        st.warning("⚠️ Required data not found. Please start the journey from the beginning.")
        if st.button("Go to Start"):
            st.session_state.page = "start"  # Navigate to your first page
            st.rerun()
        st.stop()

    st.title("📖 Your Personalized Narrative Journey")

    # --- Initialize State ---
    scores = st.session_state.sc_scores
    pdata = st.session_state.personal_data

    if "current_scene" not in st.session_state:
        st.session_state.current_scene = 1
        st.session_state.story_text = {2: None, 4: None, 6: None}
        st.session_state.generated_audio = {}
        st.session_state.reflections = {}
        st.session_state.ongoing_story = ""
        st.session_state.story_sections = []
        st.session_state.scene_paragraph_idx = {}

    # --- All Helper Functions MUST be defined inside `render` ---

    neutral_scenes = {
        1: """The room was located in the basement of the building. Access was through a heavy door with a numeric keypad lock. Inside, the air was consistently cool and dry, maintained by a climate control system that hummed at a low, steady frequency. The only illumination came from long fluorescent light panels on the ceiling, which cast an even, shadowless light across the space.
        The floor was polished concrete, and the walls were painted a uniform off-white. Along the length of the room, there were six rows of metal shelving units, bolted to the floor and ceiling. Each unit was six shelves high and divided into sections by thin metal partitions. The shelves were filled with cardboard archive boxes of a standard size and color, a neutral beige. 
        Every box had a white label affixed to its front. On each label, a sequence of alphanumeric characters was printed in black ink, corresponding to a location index in a database. The boxes were aligned flush with the edge of the shelves. A person entered the room, their footsteps making no sound on the concrete floor. 
        They consulted a tablet, then walked to the third aisle, fourth unit, second shelf from the top. They located the box with the label FIN-Q3-2024-B7. Using both hands, they slid the box forward, off the shelf, and placed it onto a rolling metal cart that had been brought in. The box was then wheeled back towards the door. After exiting, the door was closed, and the lock engaged with an audible click, leaving the room in its previous state of order and silence.
        """,
        
        3: """The control room overlooked the sedimentation tanks through a large pane of reinforced glass. Inside, the environment was sterile and quiet. A series of monitors were arranged in a semi-circle on a long console. Each monitor displayed a different data feed: flow rates, pH levels, turbidity measurements, and chlorine concentrations. 
        The numbers and graphs updated in real-time, with green figures indicating values within the acceptable range and yellow figures indicating a deviation requiring monitoring. No figures were red. On the main screen, a schematic of the entire plant was displayed.Blue lines showed the path of water moving from the primary intake pumps, through the coagulation and flocculation basins, and into the sedimentation tanks visible through the window. 
        Small icons on the schematic blinked at a regular interval, signifying that each piece of equipment was online and operational. The operator on duty observed the screens, periodically making entries into a digital logbook on a separate computer. The keyboard clicks were the only sharp sounds in the room. Outside, the water in the large concrete tanks was still and grey. 
        A mechanical scraper arm, extending across the width of a tank, moved very slowly from one end to the other. Its function was to collect settled solids from the bottom of the tank and move them towards a collection hopper. The arm’s progress was almost imperceptible unless one focused on its position relative to a fixed point on the tank’s edge. After completing its pass, it would reverse direction and begin the process again. The cycle was continuous, operating 24 hours a day.
        """,
        
        5: """The book was placed on the copy stand to the left of the scanner. It was an old textbook, its cover showing signs of wear along the spine and corners. The scanner was a planetary model, with an overhead camera and two lighting arrays positioned at 45-degree angles to prevent glare. A V-shaped cradle supported the book, allowing its pages to lie as flat as possible without putting stress on the binding. 
        The operator wore thin, white cotton gloves to avoid transferring oils to the paper. The process began. The operator turned to the first page, using a thin, flat tool made of bone to gently hold the page down at the edge. They checked the focus on the monitor, then pressed a foot pedal. The lights flashed for a fraction of a second, and the image of the page appeared on the screen. 
        The software automatically cropped and de-skewed the image, saving it as a TIFF file in a designated folder. The file was named 0001.tiff. The operator then turned to the next page. They carefully lifted the page from the right side and laid it down on the left, ensuring it was aligned within the guides on the cradle. Again, the foot pedal was pressed. The lights flashed. 
        The image appeared, was processed, and was saved as 0002.tiff. This sequence of actions—turning the page, checking alignment, pressing the pedal—was repeated without variation. The only goal was to create a complete and accurate digital surrogate of the physical object, one page at a time."""
    }
    
    neutral_question = "Did this scene evoke any particular feelings or thoughts for you? If so, please share them below."
    
    static_reflective_questions = {
        2: ("How much do you relate to the main character in this scene ?", "When you think about the main character's struggle in this scene, did you feel like they deserved understanding or support ? Why or why not ?"),
        4: ("How much do you relate to the main character in this scene ?", "When you think about the main character's struggle in this scene, did you feel like they deserved understanding or support ? Why or why not ?"),
        6: ("How much do you relate to the main character in this scene ?", "When you think about the main character's struggle in this scene, did you feel like they deserved understanding or support ? Why or why not ?")
    }

    def get_kindness_story(score):
        if score <= 7:
            return """Ananya stood frozen in front of the mirror in her cramped hostel room near her college. The ceiling fan creaked overhead, but her thoughts were louder, harsher. She stared at her reflection with disgust; the acne scars she couldn’t hide, the dark circles under her eyes from another night of cramming, and worst of all, the memory of how she’d snapped at her chemistry teacher.
            “You’re such a mess,” she whispered. “No wonder people lose patience with you. You can’t even control your tone.”
            She scanned her face again. The imperfections screamed back at her. “You look tired. You look like someone who tries hard and still fails. Maybe you are a failure.”
            A soft knock interrupted the spiral. Maya stood at the door holding two paper cups of cutting chai from the canteen. “You want?”
            Ananya shook her head. She didn’t deserve the comfort. She barely managed a grunt and turned away.
            Later that evening, Maya wrote something on their shared whiteboard before heading out:
            “Be as kind to yourself as you are to me when I break down.”
            Ananya read it and scoffed. “Kindness to myself? For what?” she muttered. “I haven’t done a single thing right this week.”
            That night, she found herself in front of the mirror again. The silence wasn’t peaceful. It was suffocating. Her eyes hunted for flaws; and found them easily. Her jaw clenched. Her shoulders tensed. She didn’t offer herself compassion. Not even neutrality. Just a brutal inventory of everything wrong.But she paused, just for a moment. Not because she felt better, but because she was too exhausted to continue hating herself.
            It wasn’t healing. It wasn’t growing. Just a pause. A breath before the next wave. But even that breath was something.
            """
        elif score in [8, 10]:
            return """Rishi’s project idea was rejected from his first hackathon. He didn’t throw anything or cry. He just shut his laptop with a dull thud and muttered, “Of course it wasn’t good enough. Why did I even think it had a chance?”
            He slumped back on his bed, letting the disappointment tighten in his chest like a knot. As he aimlessly flipped through his rough notes, his eyes caught a scribble in the margin: “Even the Himalayas weren’t built in a day.”
            It was his handwriting — overly hopeful, overly naive. He rolled his eyes. “Wow, you really thought writing cheesy lines would make you capable?”
            The words didn’t comfort him. They embarrassed him. He felt stupid for having believed he was ever building anything worth noticing.
            Still, he drifted to the kitchen, made a half-hearted cup of chai, and sat out on the balcony as the evening slipped in.
            There was no inspiration, no clarity. Just the hum of self-criticism. “You always fall short. Always.”
            But for once, he didn’t pile on. He didn’t praise himself either — he just stayed quiet. Maybe out of fatigue. Maybe because he’d already said enough.
            The failure still stung. And he still believed it reflected something about him. But for tonight, at least, he let the judgment go quiet. Not out of kindness — just surrender.
            It wasn't a relief. But it was a pause.
            """
        elif score in [11, 14]:
            return """Megha had always walked a fine line with her emotions, like a tightrope she couldn’t quite step off. Preparing for the CAT exams tested her more than school ever had. After every silly mistake, she’d sigh and mutter, “You should’ve seen that coming,” or “You’re falling behind again.”
            Her coaching centre buzzed with competition. Everyone seemed to know more, solve faster, and stress less. One day, after stumbling through a mock test, Megha slipped into the restroom and let a few quiet tears fall. “You’ve got to toughen up,” she told herself, but the words didn’t hit as hard as they used to.
            That night, wrapped in her blanket with a worn copy of One Indian Girl, she reread a line she’d underlined months ago: “This is how your mind plays games with you...” It didn’t fix things, but it made her pause. Maybe not every thought was true.
            She still scolded herself sometimes; for not sticking to schedules, for missing revisions. But now she followed it with a breath. An apology. A soft promise to do better, not perfectly.
            The day she fumbled an online interview question, she felt the old panic rising. But instead of spiraling, she opened her diary and wrote, “I didn’t answer well. But I showed up. I stayed.”
            The inner critic hadn’t vanished. But it no longer shouted alone. A quieter voice had begun to speak — not always, not loudly, but enough to be heard.
            And together, they were learning balance.
            """
        elif score in [15, 17]:
            return """Aarav had just returned from Sarojini Nagar, his bag stuffed with joyful bargains- a denim jacket for ₹250 and drawing notebooks for his sister. He was humming a Shah Rukh Khan tune when he spotted the disaster: biryani spilled across his handwritten exam notes.
            He froze. But only for a second. Then he smiled wryly and said aloud, “Well, that’s one way to add flavor to studying.”
            He gently cleaned up the mess, reminding himself, “It’s okay. These are just notes. My learning isn’t ruined — it’s just taking a little detour.” He reopened his laptop. Most of the material could be re-downloaded. What couldn’t, he’d rework patiently.
            That evening, he sat sketching a mandala alongside his sister while Chak De! India played silently in the background. There was no tension in his shoulders, just quiet focus.
            He thought about his day; the rush of the market, the spill, the recovery. And instead of criticism, he offered himself credit.
            In his journal, he wrote: “Things went a little off today, but I handled it with grace. That matters more than perfection.”
            The mistake wasn’t a verdict. It was a moment. And he met it with care. In the days that followed, Aarav began planting small seeds of self-kindness in others, too:When a classmate panicked after forgetting an assignment, Aarav handed over his own half-eaten muffin and said with a smile, “You forgot a deadline. You didn’t fail as a person.”He made a casual habit of ending his group chats with messages like “Take breaks. You’re not a robot” or “Proud of us for just trying.”
            During exam prep, he brought extra chai and quietly placed a sticky note on a friend’s table: “You deserve kindness, even when you're behind schedule.”
            When someone said “I messed everything up today,” he’d reply, “We all do. What matters is that you showed up. That’s never nothing.”
            Aarav knew now- compassion wasn’t just a feeling. It was a practice. And with each small gesture, he invited others to treat themselves like they’d treat a friend — gently, patiently, and without harsh edits. Because, as he’d written in his notebook’s new first page:
            “Perfection is brittle. Kindness? That’s what lasts.”
            """
        else:
            return """Tanya was on her terrace, painting a mandala as her phone buzzed with entrance result updates. She had missed her target college by a few marks.
            Her friends were already deep into hostel group chats, course selections, and shopping lists.
            The old Tanya might’ve buried herself under a blanket, numbing the ache with endless anime edits. But today, she wrapped herself in softness. She made warm soup, rewatched a Shah Rukh Khan classic, and whispered kindly to herself, “It’s okay to be sad. This moment deserves your tenderness.”
            She dialed her older cousin, needing comfort more than answers. He reminded her, “Even Shah Rukh took years before DDLJ happened.”
            Tanya let the smile rise slowly through the tears. “I’m still writing my story,” she told herself. “And one missed scene doesn’t ruin the whole film.”
            She wasn’t where she had planned to be- but she held herself like someone who still belonged. And that, she decided, was enough for today.
            In the weeks that followed, Tanya carried that softness with her and began quietly offering it to others, too: When a friend messaged her in a panic about a poor mock test score, Tanya simply replied, “That number doesn’t get to decide your worth. Take a breath. You’re more than this moment.” She began doodling little kindness reminders on the corners of her old notebooks — “Be gentle with your pace,” or “Pause before you punish yourself” and left them on the library table for others to find.In her entrance exam group chat, whenever stress spiraled, she’d drop a note: “If you spoke to a friend the way you speak to yourself, would they feel safe? Be that friend to you.” And once a week, she started posting simple, honest reflections on her Instagram story: a photo of her mandala, a line from her journal, or just, “Today was hard. I was kind to myself anyway.”

            Tanya wasn’t preaching. She was practicing.
            And by living gently, out loud; she reminded others that failure didn’t mean they were unworthy. It just meant they were human.
            And being human, Tanya now knew, was a story worth showing up for; even when the scene wasn’t perfect.
            """
    def get_humanity_story(score):
        if score <= 7:
            return """Riya sat cross-legged on her bed, her sketchpad untouched beside her. She had flunked an important college assignment. Outside, the world seemed to spin without her- Instagram stories of friends laughing in Sarojini Nagar, café boomerangs, reels celebrating ‘productive Sundays’. But in her room, the silence pressed in.
            “Why is it always me?” she whispered, voice cracking. “Why can’t I just get it right for once?”
            She didn’t message anyone. What was the point? No one would understand. Everyone else seemed to be thriving- submitting assignments on time, acing tests, smiling without faking it. She felt like the only one constantly falling short, the only one too weak to keep up.
            That night, while scrolling in a daze, she stumbled upon a Reddit thread where strangers shared their bad weeks. One user wrote, “Failed my pottery project. Feel like giving up.”
            Riya read it, then scrolled past. “Yeah, but that’s not the same,” she muttered. “They’ll probably bounce back tomorrow. I’m just… stuck.”
            Her chest felt tight, her mind louder than ever. The thought of explaining herself felt exhausting. She wasn’t ready to talk. Maybe she refuses to accept that failure was a common experience - “a part and parcel of life”.
            As she shut her sketchpad, she tried to remember a quote — something about not giving up. She pulled the blanket over her head, swallowed the lump in her throat, and told herself, “No one gets it. Not really.”
            """
        elif score in [8, 10]:
            return """Arjun sat in his coaching class, watching others nod along with ease as the teacher explained financial ratios. Their pens moved confidently; their faces looked calm. His mind, however, was elsewhere — stuck on the rejection email he’d received that morning. Another door closed. Another silent “no.”
            He had really wanted that summer internship at that MNC. Maybe too much. Now, he wondered if he was just not cut out for this path.
            During the break, he crossed paths with Priya, a quiet girl from the back row. She gave a half-smile and said, “Didn’t get the startup one either. Just wanted to disappear for a bit.”
            Arjun nodded politely, but the words didn’t reach far. “She’s probably handling it better,” he thought. “Everyone else seems to move on. I’m the only one still stuck.”
            Back in class, he stared blankly at the board, barely hearing the lecture. He looked around and felt out of place, like someone pretending to belong in a room he hadn’t earned a seat in. Their confidence looked effortless. His doubt felt permanent.
            That evening, sipping chai at a roadside stall, he tried to distract himself by remembering a line from Dear Zindagi: “Don’t let the past blackmail your present to ruin a beautiful future.”
            But it rang hollow. Beautiful future? He wasn’t even sure if he had a present worth holding onto.
            He still felt left out. And the feeling wasn’t going away. Everyone else seemed to be building, moving, rising.
            Arjun stared at the steam rising from his cup. Alone in the noise of the street, he mumbled, “But then Priya also didn’t make it. Maybe next time we get lucky.”
            """
        elif score in [11,14]:
            return """Meera clutched her guitar a little tighter as she stepped into her music studio . The last few compositions she’d made went flat during performance. She hadn’t told anyone, but it stung; music was supposed to bring her peace, not feel like another thing she was failing at.
            As the class began, she stayed quiet, unsure whether she belonged here at all. Her fingers moved stiffly over the guitar strings, her mind replaying the fractures in her work and wondering if maybe she just wasn’t made for this.
            Midway through, their teacher, an older artist with blistered fingers,  paused to share a story. “My first ten compositions,” he laughed, “were a flop. I still listen to them. They remind me where I started.”
            It made something soften in her.
            During the chai break, a student next to her sighed and held up a flute. “This one creaked too,” she said. “Felt like a personal attack.”
            Meera chuckled. “Same here.” It wasn’t a grand moment, but it made her feel less like she was failing alone.
            That night, at home, she pulled out one of her guitars once again and began to play. Her nani’s old voice echoed in her head, quoting SRK: “Picture abhi baaki hai, mere dost.”
            She wasn’t sure how many more times she would fail. But for the first time, that didn’t feel like a reason to stop.
            As she scrolled through a post about ISRO’s early failed lunar missions, she smiled faintly. Even the sky doesn't always cooperate.
            Maybe failures were a part of the journey. Maybe everyone, somewhere, was mending something.
            """
        elif score in [15, 17]:
            return """Nikhil stood frozen in front of the projector screen, mid-pitch. He had rehearsed for weeks, memorizing every transition, polishing every slide. But one forgotten line led to a stammer, and then a blank. The rest of the pitch felt like he was wading through fog.
            The meeting ended with polite nods and a thank-you. But inside, Nikhil felt a sting of disappointment; not crushing, but familiar.
            Later, at a café near Hauz Khas, his mentor stirred her cold coffee and offered a soft smile. “You know Amitabh Bachchan was rejected in his first voice test, and his first eleven films didn’t work out?” she said. “And now we all quote him like scripture.”
            The others around the table chimed in, one after another. A girl confessed to spilling coffee on a client’s report. A boy laughed about accidentally sending the wrong UPI link in his first startup job.
            Instead of shame, there was laughter. Not at the mistakes;  but at the shared experience of being human.
            That night, Nikhil rewatched Dangal and paused at the line, “Mhaari chhoriyaan chhoron se kam hain ke?”
            He smiled. Maybe his anxiety, his fumble, wasn't smaller or weaker. Just part of the process.
            He wrote in his journal: “I stumbled today. But so does everyone. And they still keep going.”
            The pitch no longer felt like a failure. It felt like something many had lived and learned from.
            And in that shared messiness, he found something solid to stand on.
            In the weeks that followed, Nikhil started doing small things: After practice pitches, he asked, “Want to share one thing you messed up and one thing you did well?” It lightened the mood, turned pressure into participation. He started a message thread called #FirstFailsOnly, where peers shared early disasters and what they learned. It began as jokes, but grew into reflections.
            When someone blanked during a mock pitch, he didn’t offer advice first. He simply said, “Same happened to me last month. Want to laugh about it before we fix it?”


            And slowly, in those simple gestures, he helped others do what he had begun to do himself:
            Let go of perfection and hold on to each other.
            """
        else:
            return """Priya’s promotion from intern to full time didn’t come through. She had poured in long hours, skipped her cousin’s wedding prep, and met every deadline. The news stung,  but it didn’t break her.
            Her mother sat beside her with chai and a warm smile. “Even ISRO didn’t land Chandrayaan on the moon the first time,” she said. “But they still made the world watch when they did. India ka jhanda lehraya — and so will yours, beta.”
            Priya nodded, the words settling gently in her chest. Instead of sulking, she stepped out for a walk in Lodhi Garden. The breeze felt like a small kindness. She recalled her mentor’s voice: “You’re not behind. You’re just becoming.”
            Later that evening, she curled up on the sofa and rewatched Swades. As SRK said, “Main nahi maanta humara desh duniya se kisi bhi maamle mein kam hai,” she whispered along, but this time, to herself.
            She wasn’t falling short. She was simply part of a bigger rhythm, one where setbacks weren’t shameful — just shared.
            While sipping her second cup of chai, she opened Instagram. A friend had posted about getting rejected by an MNC. Another wrote about a breakup. Priya smiled, not in amusement, but in recognition.
            Everyone was carrying something. Everyone was trying. The world wasn’t about flawless wins — it was about showing up anyway.
            That night, she journaled: “Today, I felt left out. But I also took care of myself. And I saw others doing the same.”
            She didn’t pretend everything was fine. But she didn’t feel alone in her sadness either.
            Her heart had grown quiet — not because it stopped aching, but because it understood: no one walks through this life unscathed.
            And we don’t have to. Not alone.
            In the weeks that followed, Priya began creating small spaces for others to feel less alone, too: She started a “Setback Saturdays” thread in her office Slack- a space where teammates could casually share one thing that hadn’t gone well that week, paired with one thing they were still proud of.
            During chai breaks, instead of jumping to pep-talks, she’d ask gently: “Want to vent or want company?”
            Just holding space became her quiet offering. On Instagram, she began posting small, honest reflections. Not curated wins, just real moments. A line from her journal. A half-burnt toast. A caption that simply read: “Learning as I go.”
            And when friends spiraled after rejections, she didn’t give advice first. She shared her own story. Not to compare, but to connect.

            Because Priya knew now: sometimes, healing begins not with solutions, but with someone saying, “Me too. I get it.”
            And in choosing to be that someone — she helped others remember they were never alone to begin with.
            """

    def get_mindfulness_story(score):
        if score <= 7:
            return """Tanishq had poured everything he had into a business idea, an eco-friendly courier bag made of starch. He believed in it, saw its potential. But at the investor pitch in Mumbai, the judges didn’t share his vision.
            “Too idealistic,” one of them said, barely glancing up. Another scrolled through his phone, uninterested.
            That night, Tanishq couldn’t sleep. His thoughts circled endlessly:
            “You’re a joke.”
            “You really thought you had something special?”
            “Everyone else is doing better. You’re the only one who doesn't belong.”
            He skipped the mess, silenced his phone, and lay still for hours, watching the ceiling fan spin above him. The rejection didn’t feel like feedback, it felt like proof. Proof that he wasn't smart enough, talented enough, or worth taking seriously.
            Even when his roommate brought him samosas from the canteen, he barely acknowledged it. What was the point? One failed pitch had become a verdict on his worth.
            He couldn’t separate what happened from who he was. The line between the idea and himself had blurred and shattered.
            But somewhere deep inside, beneath the noise, a small voice murmured, “You are not just this one moment.”
            He didn’t believe it yet. It felt distant, almost fragile. But the thought lingered, soft and persistent, like light behind heavy curtains.
            Maybe the failure wasn’t the whole truth. Maybe it was just a part of the story.
            And maybe, with time, he could learn to see it that way.
            """
        elif score in [8, 10]:
            return """Ananya loved doodling mandalas and had recently applied for a design fellowship run by a Delhi-based NGO. When she didn’t get selected, she shrugged in front of her mother, saying, “It’s okay, I didn’t expect much anyway.”
            But that evening, she sat frozen in front of her sketchpad, pencil untouched. Her mind didn’t just replay the rejection; it dragged out every past mistake like a playlist on loop. The school award she didn’t win. The Durga poster her teacher said looked “unfinished.” That one spelling bee in Class 4 where she misspelled “journey.”
            “Maybe I never had it,” she thought. “Maybe I’ve just been pretending all along.”
            She ignored her buzzing phone. Skipped the movie plan with her friends. Even when a Salman Khan film, the one she usually couldn’t resist; played on TV, she watched it blankly, untouched by the action and charm.
            The next morning, she opened her journal, not to write, just to fill the silence. Her pen scrawled random patterns. But then, almost by accident, she wrote: “It hurt.”
            She paused.
            And then added slowly:
            “But I’m still the girl who loves to create.”
            The sadness didn’t vanish. But for a flicker of a second, it softened. She hadn’t solved anything. But she had stopped fighting herself.
            It wasn’t healing — not yet. But maybe, just maybe, it was the first breath toward it.
            A tiny diya in the dark, reminding her: feelings aren’t facts. They’re just passing weather.
            """
        elif score in [11,14]:
            return """Dev was the kind of person who prepared thoroughly; detailed slides, timed delivery, practiced hand gestures. So when his marketing pitch at the college fest was met with blank stares and awkward silence, he walked out calmly, holding his expression steady.
            But inside, frustration boiled.
            “You should’ve done better.”
            “Maybe you’re not cut out for this.”
            He wandered the campus aimlessly — past the chaiwala’s stall, past the old gulmohar tree he used to sit under before exams. His mind kept circling the pitch, replaying the stumbles, searching for the moment it went off-track.
            A line from a mindfulness podcast floated back into his awareness: “You can feel the rain without becoming the storm.”
            He stopped near the library bench and let himself sit down. No dramatic insight. Just stillness. He noticed the tightness in his jaw, the ache behind his eyes. The self-judgment was still there, but it wasn’t yelling anymore.
            Later that evening, he messaged Bhargav. Not to vent about the pitch, just to share a new song he’d discovered. It was a small shift. But it mattered.
            He was still upset. Still second-guessing. But the pitch wasn’t all of him. It was just one scene.
            And maybe, just maybe, he could learn to let hard moments pass without letting them rewrite his entire script.
            Balance, he thought, isn’t the absence of pain. It’s the ability to pause before the spiral.
            """
        elif score in [15, 17]:
            return """Sana had worked for a month on a proposal for a pottery residency in Pondicherry. When she saw the rejection email, she blinked once, twice then gently closed the laptop.
            She exhaled slowly and said to herself, “This stings. And that’s okay.”
            Then she walked into the kitchen, made herself some nimbu-paani, and settled on the balcony. She didn’t distract herself. She didn’t deny the disappointment. Instead, she let the emotions move through her, like a slow, passing monsoon drizzle.
            Years ago, a rejection like this might’ve shaken her deeply. But today, she carried it differently. She’d learned how to hold her setbacks with kindness instead of judgment.
            While folding her dupattas, she caught herself smiling.
            “I didn’t get the residency,” she said softly, “but I also didn’t abandon myself.”
            Strength, she realized, isn’t always in pushing through. Sometimes, it’s in pausing long enough to not become the voice that hurts you the most.
            Later that week, when a friend in her art group confessed to feeling “useless” after a competition loss, Sana listened without interrupting. Then she shared her own story  not to fix, but to reflect.
            “You don’t have to be okay right away,” she said. “But don’t forget; you’re still you, even when things don’t go your way.”
            She began posting quiet reminders on their group chat now and then quotes about self-compassion, articles on rejection as redirection, and occasionally, just a simple line:
            “You can feel the rain without becoming a storm.”
            """
        else:
            return """Arav was practicing a complex sitar composition in his music class at Shantiniketan. He’d spent two weeks refining every note, coaxing the melody into shape, letting his fingers memorize the rhythm like breath.
            On the final day, just as the raag reached its peak, his fingers faltered. A jarring note rang out; sharp, misplaced and broke the silence.
            The room went still.
            Arav paused, then smiled gently.
            “Well… that note had its own idea,” he said, shrugging.
            His teacher tilted her head. “Not frustrated?”
            “I felt it,” he replied, tuning the string again, “but I’ve learned not to let a wrong note write the whole song.”
            As he walked back through the tree-lined campus, the scent of blooming champa flowers in the air, Arav felt calm. Years ago, a mistake like this would have shaken him — he’d have replayed it all evening, questioned his talent, skipped dinner.
            But now, he knew better. He could feel disappointment and still continue. Like a passing breeze, not a permanent storm. The note had slipped;  not his worth.
            He smiled inwardly. In life, some moments fall out of tune. That doesn’t mean we’re out of tune.
            Later that week, during a casual jam session, he heard a classmate groan after a missed note. Arav sat beside him and said, “You know, even seasoned artists miss beats. But they won't stop playing.”
            He began sharing small reminders with his peers:A playlist of live performances with visible imperfections.A journal corner in the practice room: “Write one kind thing to yourself after each session.”Group pauses before practice: two minutes of breath and silence, just to arrive.
            Sometimes, he'd gently remind them, “You’re not perfect. You’re the one showing up with the courage to try again.” And slowly, like the soft return of a familiar raag, acceptance began to hum through the group.
            """


    themes = [
            ("Self-Kindness vs Self-Judgment", get_kindness_story(scores["Self-Kindness vs Self-Judgment"])),
            ("Common Humanity vs Isolation", get_humanity_story(scores["Common Humanity vs Isolation"])),
            ("Mindfulness vs Overidentification", get_mindfulness_story(scores["Mindfulness vs Overidentification"])),
        ]
    themes_map = {2: themes[0], 4: themes[1], 6: themes[2]}
    
    def extract_story_from_llm_output(raw_text: str) -> str:
        """
        Extracts the core story text from the LLM's raw output,
        removing preambles and code blocks.
        """
        # Pattern to find content inside triple quotes, handling multiline text
        match = re.search(r'"""(.*?)"""', raw_text, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Fallback: if no triple quotes, assume the first long paragraph is the start
        lines = raw_text.split('\n')
        story_lines = []
        found_story = False
        for line in lines:
            # Heuristic to find the start of the story
            if len(line.strip()) > 50: # Assume a story paragraph is reasonably long
                found_story = True
            if found_story:
                story_lines.append(line)

        return "\n".join(story_lines).strip() if story_lines else raw_text.strip()

    # --- MODIFICATION: Updated to use Hugging Face client ---
    def generate_story_text(scene_idx, ongoing_story, _pdata):
        theme_name, base_template = themes_map[scene_idx]
        
        # This prompt is based on your original, successful Gemma prompt
        prompt = f"""
        You are a gentle, skilled writer who connects emotional narratives. Write a scene for the character {_pdata['name']} (age {_pdata['age']}), a {_pdata['profession']}.

        Subtly integrate the following context about the character's state of mind and background:
        - Current emotion: '{_pdata['emotion']}'
        - Perspective on family expectations: '{_pdata['family_oriented']}'

        The theme for this specific scene is: **{theme_name}**

        Here is the story so far:
        \"\"\"
        {ongoing_story}
        \"\"\"

        Please continue the narrative, using this theme template as a structural and emotional base:
        \"\"\"
        {base_template}
        \"\"\"

        ### Instructions
        1.  Personalize the theme for the character.
        2.  Keep the tone grounded and subtle, with Indian college-life cues if appropriate.
        3.  Use simple, accessible language.
        4.  The output must be 2-3 short paragraphs.
        5.  Do not repeat the base template or the ongoing story verbatim. Adapt and evolve the narrative.
        6.  The response must be **only the raw story text**. Do not include any titles, headings, or introductions like "Here is the scene...".
        """
        
        try:
            # Call the Google Generative AI API
            response = model.generate_content(prompt)
            
            # Directly return the clean text from the response
            return extract_story_from_llm_output(response.text)
            
        except Exception as e:
            st.error(f"❌ Error generating story with Gemma: {e}")
            return None


    # @st.cache_data
    # def generate_tts_audio(_text):
    #     try:
    #         tts = gTTS(text=_text, lang='en', slow=False)
    #         audio_fp = io.BytesIO()
    #         tts.write_to_fp(audio_fp)
    #         audio_fp.seek(0)
    #         return audio_fp.read()
    #     except Exception as e:
    #         st.error(f"TTS error: {e}")
    #         return None

    def display_paragraph_by_paragraph(scene_idx, full_text):
    # Split the full text into a list of paragraphs
        paras = [p.strip() for p in full_text.split("\n") if p.strip()]
        if not paras: # Handle cases with no text
            return True

        # Get the paragraph index for the current scene from session state
        key_idx = f"para_idx_{scene_idx}"
        if key_idx not in st.session_state.scene_paragraph_idx:
            st.session_state.scene_paragraph_idx[key_idx] = 0
        
        current_para_idx = st.session_state.scene_paragraph_idx[key_idx]

        # --- MODIFICATION ---
        # Instead of a loop, display only the single paragraph at the current index.
        # The previous paragraphs will be replaced on each rerun.
        st.markdown(f"<p style='padding: 1rem; border-left: 5px solid #d3d3d3; border-radius: 5px; margin-bottom: 1rem;'>{paras[current_para_idx]}</p>", unsafe_allow_html=True)
        
        # Check if there are more paragraphs left in the scene
        if current_para_idx < len(paras) - 1:
            # Show a button to advance to the next paragraph
            if st.button("Continue Reading 👇", key=f"next_para_btn_{scene_idx}"):
                st.session_state.scene_paragraph_idx[key_idx] += 1
                st.rerun()
            return False # Indicates the story section is still ongoing
        
        return True # Indicates all paragraphs for this scene have been displayed

    def show_scene(scene_idx):
        st.header(f"Scene {scene_idx} / 6")
        st.divider()

        # Determine if the current scene is a neutral, static one
        is_neutral_scene = scene_idx % 2 == 1
        full_text = None

        if is_neutral_scene:
            # --- NEUTRAL SCENE ---
            full_text = neutral_scenes[scene_idx]
            
            # **PRE-GENERATION LOGIC**
            # While the user reads this neutral scene, generate the next story scene.
            next_story_scene_idx = scene_idx + 1
            if next_story_scene_idx <= 6:
                if st.session_state.story_text.get(next_story_scene_idx) is None:
                    # This runs "in the background" from the user's perspective.
                    # The user sees the neutral text while this call completes.
                    new_text = generate_story_text(next_story_scene_idx, st.session_state.ongoing_story, pdata)
                    if new_text:
                        st.session_state.story_text[next_story_scene_idx] = new_text
                        # IMPORTANT: We only update the 'ongoing_story' state when the scene is actually displayed,
                        # not during pre-generation. We'll do that in the 'else' block below.
                    else:
                        # Store a failure marker to prevent re-tries
                        st.session_state.story_text[next_story_scene_idx] = "GENERATION_FAILED"

        else:
            # --- GENERATED STORY SCENE ---
            # Check if the text is ready (either pre-generated or needs generating now)
            if st.session_state.story_text.get(scene_idx) is None:
                # This block will only run for the very first story scene (Scene 2)
                # or if pre-generation failed.
                with st.spinner("✍️ Crafting the next part of your story... this may take a moment."):
                    new_text = generate_story_text(scene_idx, st.session_state.ongoing_story, pdata)
                    if new_text:
                        st.session_state.story_text[scene_idx] = new_text
                        # It's time to show this scene, so add it to the permanent ongoing story
                        st.session_state.ongoing_story += "\n\n" + new_text
                        st.rerun() # Rerun to display the newly fetched text
            
            full_text = st.session_state.story_text.get(scene_idx)
            
            if full_text == "GENERATION_FAILED":
                st.error("Could not generate the story for this scene. Please try refreshing the page.")
                return

        # --- UNIFIED DISPLAY, AUDIO, AND REFLECTION LOGIC ---
        if full_text:
            # Display text paragraph-by-paragraph for ALL scenes
            all_paras_shown = display_paragraph_by_paragraph(scene_idx, full_text)

            # Once all paragraphs of a scene are shown, show audio and reflection questions
            if all_paras_shown:
                # with st.spinner("Preparing audio..."):
                #     if scene_idx not in st.session_state.generated_audio:
                #         st.session_state.generated_audio[scene_idx] = generate_tts_audio(full_text)
                #     if st.session_state.generated_audio[scene_idx]:
                #         st.audio(st.session_state.generated_audio[scene_idx], format="audio/mp3")

                st.subheader("Reflection")
                if is_neutral_scene:
                    r = st.text_area(neutral_question, key=f"reflect_{scene_idx}")
                    st.session_state.reflections[f"reflect_{scene_idx}"] = r
                else:
                    q1, q2 = static_reflective_questions[scene_idx]
                    r1 = st.text_area(q1, key=f"reflect_{scene_idx}_q1")
                    r2 = st.text_area(q2, key=f"reflect_{scene_idx}_q2")
                    st.session_state.reflections[f"reflect_{scene_idx}_q1"] = r1
                    st.session_state.reflections[f"reflect_{scene_idx}_q2"] = r2
        
        # --- NAVIGATION ---
        st.divider()
        if st.button("Next Scene ➡️", key=f"next_scene_{scene_idx}"):
            if scene_idx < 6:
                st.session_state.current_scene += 1
                st.rerun()
            else:
                go_to_next_page()

    # Initial call remains the same
    show_scene(st.session_state.current_scene)
