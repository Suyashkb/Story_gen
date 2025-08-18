import streamlit as st
import io
from gtts import gTTS
from dotenv import load_dotenv
import os
import re
import time
import google.generativeai as genai
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
    
    
def get_kindness_story(score):
    if score <= 25:
        return """
            P1: 
            Ananya stood frozen in front of the mirror in her cramped hostel room near her college. The ceiling fan creaked overhead, but her thoughts were louder, harsher. She stared at her reflection with disgust; the acne scars she couldn’t hide, the dark circles under her eyes from another night of cramming, and worst of all, the memory of how she’d snapped at her chemistry teacher.
            P2:
            “You’re such a mess,” she whispered. “No wonder people lose patience with you. You can’t even control your tone.”
            She scanned her face again. The imperfections screamed back at her. “You look tired. You look like someone who tries hard and still fails. Maybe you are a failure.”
            A soft knock interrupted the spiral. Maya stood at the door holding two paper cups of cutting chai from the canteen. “You want?”
            Ananya shook her head. She didn’t deserve the comfort. She barely managed a grunt and turned away.
            Later that evening, Maya wrote something on their shared whiteboard before heading out:
            “Be as kind to yourself as you are to me when I break down.”
            Ananya read it and scoffed. “Kindness to myself? For what?” she muttered. “I haven’t done a single thing right this week.”
            P3:
            That night, she found herself in front of the mirror again. The silence wasn’t peaceful. It was suffocating. Her eyes hunted for flaws; and found them easily. Her jaw clenched. Her shoulders tensed. She didn’t offer herself compassion. Not even neutrality. Just a brutal inventory of everything wrong.But she paused, just for a moment. Not because she felt better, but because she was too exhausted to continue hating herself.
            It wasn’t healing. It wasn’t growing. Just a pause. A breath before the next wave. But even that breath was something.
            """
    # elif score in [18, 25]:
    #     return """
    #         P1: Rishi’s project idea was rejected from his first hackathon. He didn’t throw anything or cry. He just shut his laptop with a dull thud and muttered, 
    #         P2:
    #         “Of course it wasn’t good enough. Why did I even think it had a chance?”
    #         He slumped back on his bed, letting the disappointment tighten in his chest like a knot. As he aimlessly flipped through his rough notes, his eyes caught a scribble in the margin: “Even the Himalayas weren’t built in a day.”
    #         It was his handwriting — overly hopeful, overly naive. He rolled his eyes. “Wow, you really thought writing cheesy lines would make you capable?”
    #         The words didn’t comfort him. They embarrassed him. He felt stupid for having believed he was ever building anything worth noticing.
    #         Still, he drifted to the kitchen, made a half-hearted cup of chai, and sat out on the balcony as the evening slipped in.
    #         There was no inspiration, no clarity. Just the hum of self-criticism. “You always fall short. Always.”
    #         P3:
    #         But for once, he didn’t pile on. He didn’t praise himself either — he just stayed quiet. Maybe out of fatigue. Maybe because he’d already said enough.
    #         The failure still stung. And he still believed it reflected something about him. But for tonight, at least, he let the judgment go quiet. Not out of kindness — just surrender.
    #         It wasn't a relief. But it was a pause.
    #         """
    elif score in [26, 34]:
        return """
            P1
            Megha had always walked a fine line with her emotions, like a tightrope she couldn’t quite step off. Preparing for the CAT exams tested her more than school ever had. After every silly mistake, she’d sigh and mutter, 
            P2
            “You should’ve seen that coming,” or “You’re falling behind again.”
            Her coaching centre buzzed with competition. Everyone seemed to know more, solve faster, and stress less. One day, after stumbling through a mock test, Megha slipped into the restroom and let a few quiet tears fall. “You’ve got to toughen up,” she told herself, but the words didn’t hit as hard as they used to.
            That night, wrapped in her blanket with a worn copy of One Indian Girl, she reread a line she’d underlined months ago: “This is how your mind plays games with you...” It didn’t fix things, but it made her pause. Maybe not every thought was true.
            P3
            She still scolded herself sometimes; for not sticking to schedules, for missing revisions. But now she followed it with a breath. An apology. A soft promise to do better, not perfectly.
            The day she fumbled an online interview question, she felt the old panic rising. But instead of spiraling, she opened her diary and wrote, “I didn’t answer well. But I showed up. I stayed.”
            The inner critic hadn’t vanished. But it no longer shouted alone. A quieter voice had begun to speak — not always, not loudly, but enough to be heard.
            And together, they were learning balance.

        """
    # elif score in [35, 42]:
    #     return """
    #         P1
    #         Aarav had just returned from Sarojini Nagar, his bag stuffed with joyful bargains- a denim jacket for ₹250 and drawing notebooks for his sister. He was humming a Shah Rukh Khan tune when he spotted the disaster: biryani spilled across his handwritten exam notes.
    #         He froze. But only for a second. Then he smiled wryly and said aloud, 
    #         P2
    #         “Well, that’s one way to add flavor to studying.”
    #         He gently cleaned up the mess, reminding himself, “It’s okay. These are just notes. My learning isn’t ruined — it’s just taking a little detour.” He reopened his laptop. Most of the material could be re-downloaded. What couldn’t, he’d rework patiently.
    #         That evening, he sat sketching a mandala alongside his sister while Chak De! India played silently in the background. There was no tension in his shoulders, just quiet focus.
    #         He thought about his day; the rush of the market, the spill, the recovery. And instead of criticism, he offered himself credit.
    #         In his journal, he wrote: “Things went a little off today, but I handled it with grace. That matters more than perfection.”
    #         The mistake wasn’t a verdict. It was a moment. And he met it with care. In the days that followed, Aarav began planting small seeds of self-kindness in others, too:When a classmate panicked after forgetting an assignment, Aarav handed over his own half-eaten muffin and said with a smile, “You forgot a deadline. You didn’t fail as a person.”He made a casual habit of ending his group chats with messages like “Take breaks. You’re not a robot” or “Proud of us for just trying.”
    #         During exam prep, he brought extra chai and quietly placed a sticky note on a friend’s table: “You deserve kindness, even when you're behind schedule.”
    #         When someone said “I messed everything up today,” he’d reply, “We all do. What matters is that you showed up. That’s never nothing.”
    #         P3
    #         Aarav knew now- compassion wasn’t just a feeling. It was a practice. And with each small gesture, he invited others to treat themselves like they’d treat a friend — gently, patiently, and without harsh edits. Because, as he’d written in his notebook’s new first page:
    #         “Perfection is brittle. Kindness? That’s what lasts.”

    #     """
    else:
        return """
            P1
            Tanya was on her terrace, painting a mandala as her phone buzzed with entrance result updates. She had missed her target college by a few marks.
            Her friends were already deep into hostel group chats, course selections, and shopping lists.
            The old Tanya might’ve buried herself under a blanket, numbing the ache with endless anime edits. But today, she wrapped herself in softness. She made warm soup, rewatched a Shah Rukh Khan classic, and whispered kindly to herself,
            P2
            “It’s okay to be sad. This moment deserves your tenderness.”
            She dialed her older cousin, needing comfort more than answers. He reminded her, “Even Shah Rukh took years before DDLJ happened.”
            Tanya let the smile rise slowly through the tears. “I’m still writing my story,” she told herself. “And one missed scene doesn’t ruin the whole film.”
            She wasn’t where she had planned to be- but she held herself like someone who still belonged. And that, she decided, was enough for today.
            In the weeks that followed, Tanya carried that softness with her and began quietly offering it to others, too: When a friend messaged her in a panic about a poor mock test score, Tanya simply replied, “That number doesn’t get to decide your worth. Take a breath. You’re more than this moment.” She began doodling little kindness reminders on the corners of her old notebooks — “Be gentle with your pace,” or “Pause before you punish yourself” and left them on the library table for others to find.In her entrance exam group chat, whenever stress spiraled, she’d drop a note: “If you spoke to a friend the way you speak to yourself, would they feel safe? Be that friend to you.” And once a week, she started posting simple, honest reflections on her Instagram story: a photo of her mandala, a line from her journal, or just, “Today was hard. I was kind to myself anyway.”
            P3
            Tanya wasn’t preaching. She was practicing.
            And by living gently, out loud; she reminded others that failure didn’t mean they were unworthy. It just meant they were human.
            And being human, Tanya now knew, was a story worth showing up for; even when the scene wasn’t perfect.
            """
def get_humanity_story(score):
    if score <= 20:
        return """
        P1
        Riya sat cross-legged on her bed, her sketchpad untouched beside her. She had flunked an important college assignment. Outside, the world seemed to spin without her- Instagram stories of friends laughing in Sarojini Nagar, café boomerangs, reels celebrating ‘productive Sundays’. But in her room, the silence pressed in.
        P2
        “Why is it always me?” she whispered, voice cracking. “Why can’t I just get it right for once?”
        She didn’t message anyone. What was the point? No one would understand. Everyone else seemed to be thriving- submitting assignments on time, acing tests, smiling without faking it. She felt like the only one constantly falling short, the only one too weak to keep up.
        That night, while scrolling in a daze, she stumbled upon a Reddit thread where strangers shared their bad weeks. One user wrote, “Failed my pottery project. Feel like giving up.”
        Riya read it, then scrolled past. “Yeah, but that’s not the same,” she muttered. “They’ll probably bounce back tomorrow. I’m just… stuck.”
        Her chest felt tight, her mind louder than ever. The thought of explaining herself felt exhausting. She wasn’t ready to talk. Maybe she refuses to accept that failure was a common experience - “a part and parcel of life”.
        P3
        As she shut her sketchpad, she tried to remember a quote — something about not giving up. She pulled the blanket over her head, swallowed the lump in her throat, and told herself, “No one gets it. Not really.”
"""
    # elif score in [15, 20]:
    #     return """Arjun sat in his coaching class, watching others nod along with ease as the teacher explained financial ratios. Their pens moved confidently; their faces looked calm. His mind, however, was elsewhere — stuck on the rejection email he’d received that morning. Another door closed. Another silent “no.”
    #     He had really wanted that summer internship at that MNC. Maybe too much. Now, he wondered if he was just not cut out for this path.
    #     During the break, he crossed paths with Priya, a quiet girl from the back row. She gave a half-smile and said, “Didn’t get the startup one either. Just wanted to disappear for a bit.”
    #     Arjun nodded politely, but the words didn’t reach far. “She’s probably handling it better,” he thought. “Everyone else seems to move on. I’m the only one still stuck.”
    #     Back in class, he stared blankly at the board, barely hearing the lecture. He looked around and felt out of place, like someone pretending to belong in a room he hadn’t earned a seat in. Their confidence looked effortless. His doubt felt permanent.
    #     That evening, sipping chai at a roadside stall, he tried to distract himself by remembering a line from Dear Zindagi: “Don’t let the past blackmail your present to ruin a beautiful future.”
    #     But it rang hollow. Beautiful future? He wasn’t even sure if he had a present worth holding onto.
    #     He still felt left out. And the feeling wasn’t going away. Everyone else seemed to be building, moving, rising.
    #     Arjun stared at the steam rising from his cup. Alone in the noise of the street, he mumbled, “But then Priya also didn’t make it. Maybe next time we get lucky.”
    #     """
    elif score in [21,27]:
        return """
            P1
            Meera clutched her guitar a little tighter as she stepped into her music studio . The last few compositions she’d made went flat during performance. She hadn’t told anyone, but it stung; music was supposed to bring her peace, not feel like another thing she was failing at.
            As the class began, she stayed quiet, unsure whether she belonged here at all. Her fingers moved stiffly over the guitar strings, her mind replaying the fractures in her work and wondering if maybe she just wasn’t made for this.
            P2
            Midway through, their teacher, an older artist with blistered fingers,  paused to share a story. “My first ten compositions,” he laughed, “were a flop. I still listen to them. They remind me where I started.”
            It made something soften in her.
            During the chai break, a student next to her sighed and held up a flute. “This one creaked too,” she said. “Felt like a personal attack.”
            Meera chuckled. “Same here.” It wasn’t a grand moment, but it made her feel less like she was failing alone.
            That night, at home, she pulled out one of her guitars once again and began to play. Her nani’s old voice echoed in her head, quoting SRK: “Picture abhi baaki hai, mere dost.”
            P3
            She wasn’t sure how many more times she would fail. But for the first time, that didn’t feel like a reason to stop.
            As she scrolled through a post about ISRO’s early failed lunar missions, she smiled faintly. Even the sky doesn't always cooperate.
            Maybe failures were a part of the journey. Maybe everyone, somewhere, was mending something.
            """
    # elif score in [28, 33]:
    #     return """Nikhil stood frozen in front of the projector screen, mid-pitch. He had rehearsed for weeks, memorizing every transition, polishing every slide. But one forgotten line led to a stammer, and then a blank. The rest of the pitch felt like he was wading through fog.
    #     The meeting ended with polite nods and a thank-you. But inside, Nikhil felt a sting of disappointment; not crushing, but familiar.
    #     Later, at a café near Hauz Khas, his mentor stirred her cold coffee and offered a soft smile. “You know Amitabh Bachchan was rejected in his first voice test, and his first eleven films didn’t work out?” she said. “And now we all quote him like scripture.”
    #     The others around the table chimed in, one after another. A girl confessed to spilling coffee on a client’s report. A boy laughed about accidentally sending the wrong UPI link in his first startup job.
    #     Instead of shame, there was laughter. Not at the mistakes;  but at the shared experience of being human.
    #     That night, Nikhil rewatched Dangal and paused at the line, “Mhaari chhoriyaan chhoron se kam hain ke?”
    #     He smiled. Maybe his anxiety, his fumble, wasn't smaller or weaker. Just part of the process.
    #     He wrote in his journal: “I stumbled today. But so does everyone. And they still keep going.”
    #     The pitch no longer felt like a failure. It felt like something many had lived and learned from.
    #     And in that shared messiness, he found something solid to stand on.
    #     In the weeks that followed, Nikhil started doing small things: After practice pitches, he asked, “Want to share one thing you messed up and one thing you did well?” It lightened the mood, turned pressure into participation. He started a message thread called #FirstFailsOnly, where peers shared early disasters and what they learned. It began as jokes, but grew into reflections.
    #     When someone blanked during a mock pitch, he didn’t offer advice first. He simply said, “Same happened to me last month. Want to laugh about it before we fix it?”


    #     And slowly, in those simple gestures, he helped others do what he had begun to do himself:
    #     Let go of perfection and hold on to each other.
    #     """
    else:
        return """P1
Priya’s promotion from intern to full time didn’t come through. She had poured in long hours, skipped her cousin’s wedding prep, and met every deadline. The news stung,  but it didn’t break her.
Her mother sat beside her with chai and a warm smile. “Even ISRO didn’t land Chandrayaan on the moon the first time,” she said. “But they still made the world watch when they did. India ka jhanda lehraya — and so will yours, beta.”
P2
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
P3
Just holding space became her quiet offering. On Instagram, she began posting small, honest reflections. Not curated wins, just real moments. A line from her journal. A half-burnt toast. A caption that simply read: “Learning as I go.”
And when friends spiraled after rejections, she didn’t give advice first. She shared her own story. Not to compare, but to connect.


Because Priya knew now: sometimes, healing begins not with solutions, but with someone saying, “Me too. I get it.”
And in choosing to be that someone — she helped others remember they were never alone to begin with.

"""

def get_mindfulness_story(score):
    if score <= 20:
        return """
P1
Tanishq had poured everything he had into a business idea, an eco-friendly courier bag made of starch. He believed in it, saw its potential. But at the investor pitch in Mumbai, the judges didn’t share his vision.
p2
“Too idealistic,” one of them said, barely glancing up. Another scrolled through his phone, uninterested.
That night, Tanishq couldn’t sleep. His thoughts circled endlessly:
 “You’re a joke.”
 “You really thought you had something special?”
 “Everyone else is doing better. You’re the only one who doesn't belong.”
He skipped the mess, silenced his phone, and lay still for hours, watching the ceiling fan spin above him. The rejection didn’t feel like feedback, it felt like proof. Proof that he wasn't smart enough, talented enough, or worth taking seriously.
Even when his roommate brought him samosas from the canteen, he barely acknowledged it. What was the point? One failed pitch had become a verdict on his worth.
He couldn’t separate what happened from who he was. The line between the idea and himself had blurred and shattered.
p3
Beneath the crushing silence, a single, desperate thought clawed for space: “You are not just this failure.”
He didn’t believe it. The idea felt brittle—ready to snap beneath the weight of self-disgust.
Still, it flickered on, stubborn as a heartbeat in darkness.
Maybe there was more to him than this ruin.
Maybe.
"""
    # elif score in [15, 20]:
    #     return """Ananya loved doodling mandalas and had recently applied for a design fellowship run by a Delhi-based NGO. When she didn’t get selected, she shrugged in front of her mother, saying, “It’s okay, I didn’t expect much anyway.”
    #     But that evening, she sat frozen in front of her sketchpad, pencil untouched. Her mind didn’t just replay the rejection; it dragged out every past mistake like a playlist on loop. The school award she didn’t win. The Durga poster her teacher said looked “unfinished.” That one spelling bee in Class 4 where she misspelled “journey.”
    #     “Maybe I never had it,” she thought. “Maybe I’ve just been pretending all along.”
    #     She ignored her buzzing phone. Skipped the movie plan with her friends. Even when a Salman Khan film, the one she usually couldn’t resist; played on TV, she watched it blankly, untouched by the action and charm.
    #     The next morning, she opened her journal, not to write, just to fill the silence. Her pen scrawled random patterns. But then, almost by accident, she wrote: “It hurt.”
    #     She paused.
    #     And then added slowly:
    #     “But I’m still the girl who loves to create.”
    #     The sadness didn’t vanish. But for a flicker of a second, it softened. She hadn’t solved anything. But she had stopped fighting herself.
    #     It wasn’t healing — not yet. But maybe, just maybe, it was the first breath toward it.
    #     A tiny diya in the dark, reminding her: feelings aren’t facts. They’re just passing weather.
    #     """
    elif score in [21,27]:
        return """
            P1
            Dev was the kind of person who prepared thoroughly; detailed slides, timed delivery, practiced hand gestures. So when his marketing pitch at the college fest was met with blank stares and awkward silence, he walked out calmly, holding his expression steady.
            P2
            But inside, frustration boiled.
            “You should’ve done better.”
            “Maybe you’re not cut out for this.”
            He wandered the campus aimlessly — past the chaiwala’s stall, past the old gulmohar tree he used to sit under before exams. His mind kept circling the pitch, replaying the stumbles, searching for the moment it went off-track.
            A line from a mindfulness podcast floated back into his awareness: “You can feel the rain without becoming the storm.”
            He stopped near the library bench and let himself sit down. No dramatic insight. Just stillness. He noticed the tightness in his jaw, the ache behind his eyes. The self-judgment was still there, but it wasn’t yelling anymore.
            p3
            Later that evening, he messaged Bhargav. Not to vent about the pitch, just to share a new song he’d discovered. It was a small shift. But it mattered.
            He was still upset. Still second-guessing. But the pitch wasn’t all of him. It was just one scene.
            And maybe, just maybe, he could learn to let hard moments pass without letting them rewrite his entire script.
            Balance, he thought, isn’t the absence of pain. It’s the ability to pause before the spiral.
            """
    # elif score in [28, 33]:
    #     return """Sana had worked for a month on a proposal for a pottery residency in Pondicherry. When she saw the rejection email, she blinked once, twice then gently closed the laptop.
    #     She exhaled slowly and said to herself, “This stings. And that’s okay.”
    #     Then she walked into the kitchen, made herself some nimbu-paani, and settled on the balcony. She didn’t distract herself. She didn’t deny the disappointment. Instead, she let the emotions move through her, like a slow, passing monsoon drizzle.
    #     Years ago, a rejection like this might’ve shaken her deeply. But today, she carried it differently. She’d learned how to hold her setbacks with kindness instead of judgment.
    #     While folding her dupattas, she caught herself smiling.
    #     “I didn’t get the residency,” she said softly, “but I also didn’t abandon myself.”
    #     Strength, she realized, isn’t always in pushing through. Sometimes, it’s in pausing long enough to not become the voice that hurts you the most.
    #     Later that week, when a friend in her art group confessed to feeling “useless” after a competition loss, Sana listened without interrupting. Then she shared her own story  not to fix, but to reflect.
    #     “You don’t have to be okay right away,” she said. “But don’t forget; you’re still you, even when things don’t go your way.”
    #     She began posting quiet reminders on their group chat now and then quotes about self-compassion, articles on rejection as redirection, and occasionally, just a simple line:
    #     “You can feel the rain without becoming a storm.”
        
    else:
        return """
        P1
        Arav was practicing a complex sitar composition in his music class at Shantiniketan. He’d spent two weeks refining every note, coaxing the melody into shape, letting his fingers memorize the rhythm like breath.
        On the final day, just as the raag reached its peak, his fingers faltered. A jarring note rang out; sharp, misplaced and broke the silence.
        The room went still.
        P2
        Arav paused, then smiled gently.
        “Well… that note had its own idea,” he said, shrugging.
        His teacher tilted her head. “Not frustrated?”
        “I felt it,” he replied, tuning the string again, “but I’ve learned not to let a wrong note write the whole song.”
        As he walked back through the tree-lined campus, the scent of blooming champa flowers in the air, Arav felt calm. Years ago, a mistake like this would have shaken him — he’d have replayed it all evening, questioned his talent, skipped dinner.
        But now, he knew better. He could feel disappointment and still continue. Like a passing breeze, not a permanent storm. The note had slipped;  not his worth.
        He smiled inwardly. In life, some moments fall out of tune. That doesn’t mean we’re out of tune.
        P3
        Later that week, during a casual jam session, he heard a classmate groan after a missed note. Arav sat beside him and said, “You know, even seasoned artists miss beats. But they won't stop playing.”
        He began sharing small reminders with his peers:A playlist of live performances with visible imperfections.A journal corner in the practice room: “Write one kind thing to yourself after each session.”Group pauses before practice: two minutes of breath and silence, just to arrive.
        Sometimes, he'd gently remind them, “You’re not perfect. You’re the one showing up with the courage to try again.” And slowly, like the soft return of a familiar raag, acceptance began to hum through the group.
        """


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

def generate_story_text(scene_idx, ongoing_story, _pdata,primary_theme_map):
        theme_name, base_template = primary_theme_map[scene_idx]
        
        # This prompt is based on your original, successful Gemma prompt
        prompt = f"""
        You are a skilled writer who connects emotional narratives. Write a scene for the character {_pdata['name']} (age {_pdata['age']}),(gender {_pdata['gender']}, a {_pdata['profession']},the first person they reach out to {_pdata['first_person']}
        Other than the main character, use the name of the provided first person they reach out to in their difficult times and refer to all more characters in third person (do not specify more names).
        try to subtly integrate the following context about the character's state of mind and background, these are the responses to their question :
        - Is there anything on your mind right now ? '{_pdata['emotion']}'
        - Perspective on family expectations: '{_pdata['family_oriented']}'

        The theme for this specific scene is: **{theme_name}**

        Here is the story so far:
        \"\"\"
        {ongoing_story}
        \"\"\"

        Please continue the narrative, using this theme template as a structural, emotional base and monologues structure :
        \"\"\"
        {base_template}
        \"\"\"

        ### Instructions
        1. The base template is currenlty divided into 3 parts in which first paragraph is for context building, second has a lot of emphasis on the monologues and third paragraph has conclusion. Generate the new stories with similar structure split into 3 paragraphs.
        2.  Personalize the theme for the character.
        3.  Keep the tone grounded and subtle, with Indian college-life cues if appropriate.
        4.  Use simple, accessible language.
        5.  The output must be 3 short paragraphs.
        6.  Do not repeat the base template or the ongoing story verbatim. Adapt and evolve the narrative.
        7.  The response must be **only the raw story text**. Do not include any titles, headings, or introductions like "Here is the scene...".
        8.  Try to include monologues or internal dialogues that reflect the character's emotional state and growth.
        9.  Use the vocabulary of a middle school child (easy to understand and simple words)
        """
        
        try:
            # Call the Google Generative AI API
            response = model.generate_content(prompt)
            # Directly return the clean text from the response
            return extract_story_from_llm_output(response.text)
            
        except Exception as e:
            st.error(f"❌ Error generating story with Gemma: {e}")
            return None
        
        
def generate_kinder_monologue_text(previous_scene_text, theme_name, _pdata):
    prompt = f"""
        You are a compassionate writing coach. Your task is to rewrite this short scene, focusing on shifting the character's internal monologue towards self-kindness and compassion.

        Character Details:
        - Name: {_pdata['name']}
        - Gender: {_pdata['gender']}
        - Background: A {_pdata['profession']} feeling '{_pdata['emotion']}'.

        The theme to address is: **{theme_name}**

        Here is the original scene where the character was struggling:
        \"\"\"
        {previous_scene_text}
        \"\"\"

        ### Instructions:
        1.  **Rewrite :** Gently evolve the scene. The character is still in the same situation, but his internal reaction starts to shift, and they are more gentle with themself
        2.  **Show the Shift:** Instead of harsh self-judgment, introduce a kinder, more understanding inner voice. For example, instead of "I'm such a failure," it might become "This is hard, and it's okay that I'm struggling."
        3.  **Subtlety is Key:** The change should feel natural and earned, not sudden or preachy. It's an internal shift.
        4.  **Tone:** Maintain the grounded, realistic tone of the story.
        5.  **Format:** The output must be similar to the original scene- short paragraphs of **raw story text only**. No titles, headings, or explanations.
        """
    try:
        response = model.generate_content(prompt)
        return extract_story_from_llm_output(response.text)
    except Exception as e:
        st.error(f"❌ Error generating High K monologue: {e}")
        return None

# --- Story Flow and State Management ---
def initialize_story_flow(scores):
    if 'scene_map' in st.session_state:
        return

    # Add a view_mode to control showing story vs. questions
    st.session_state.view_mode = 'story' 
    
    KINDER_MONOLOGUE_THRESHOLD = 22
    st.session_state.scene_map = []
    
    # (The rest of your original logic is fine)
    st.session_state.scene_map.append({'number': 1, 'type': 'neutral'})
    st.session_state.scene_map.append({'number': 2, 'type': 'compassion'})
    if scores.get("Self-Kindness vs Self-Judgment", 99) < KINDER_MONOLOGUE_THRESHOLD:
        st.session_state.scene_map.append({'number': 3, 'type': 'kinder'})
        
    st.session_state.scene_map.append({'number': 4, 'type': 'neutral'})
    st.session_state.scene_map.append({'number': 5, 'type': 'compassion'})
    if scores.get("Common Humanity vs Isolation", 99) < (KINDER_MONOLOGUE_THRESHOLD-5):
        st.session_state.scene_map.append({'number': 6, 'type': 'kinder'})

    st.session_state.scene_map.append({'number': 7, 'type': 'neutral'})
    st.session_state.scene_map.append({'number': 8, 'type': 'compassion'})
    if scores.get("Mindfulness vs Overidentification", 99) < (KINDER_MONOLOGUE_THRESHOLD-5):
        st.session_state.scene_map.append({'number': 9, 'type': 'kinder'})

    st.session_state.total_scenes = len(st.session_state.scene_map)
    st.session_state.current_scene_index = 0
    st.session_state.story_text = {}
    st.session_state.ongoing_story = ""
    st.session_state.reflections = {}
    st.session_state.scene_paragraph_idx = {}
    st.session_state.appended_scenes = set()
    
# --- UI Display Functions ---
def display_paragraph_by_paragraph(scene_number, full_text):
    paras = [p.strip() for p in full_text.split("\n") if p.strip()]
    if not paras: return True

    key_idx = f"para_idx_{scene_number}"
    if key_idx not in st.session_state.scene_paragraph_idx:
        st.session_state.scene_paragraph_idx[key_idx] = 0
    
    current_para_idx = st.session_state.scene_paragraph_idx[key_idx]

    st.markdown(f"<p style='padding: 1rem; border-left: 5px solid #d3d3d3; border-radius: 5px; margin-bottom: 1rem;'>{paras[current_para_idx]}</p>", unsafe_allow_html=True)
    
    if current_para_idx < len(paras) - 1:
        if st.button("Continue Reading ->", key=f"next_para_btn_{scene_number}"):
            st.session_state.scene_paragraph_idx[key_idx] += 1
            st.rerun()
        return False
    return True

def generate_dynamic_fourth_question(theme_name, score):
    """Generates a targeted reflection question based on theme and user score."""
    
    # --- This is where you define your logic for the fourth question ---
    # You can make this as complex as you need.
    
    if theme_name == "Self-Kindness vs Self-Judgment":
        if score < 18: # Example threshold for low score
            return "The character was quite hard on themselves. What's one gentle or kind thought they could have offered themselves in that moment?"
        else: # Example for high score
            return "The character found a way to be kind to themselves. What helps you access your own kinder inner voice when you're struggling?"
            
    elif theme_name == "Common Humanity vs Isolation":
        if score < 18:
            return "Feeling isolated is a tough experience, as the character showed. What's a small reminder you can use to remember that everyone struggles at times?"
        else:
            return "The character started to realize they weren't alone. How does connecting with others, even in small ways, affect your own perspective?"

    elif theme_name == "Mindfulness vs Overidentification":
        if score < 18:
            return "The character was completely swept away by their difficult thoughts. What's one physical sensation you can focus on right now (like your feet on the floor) to ground yourself?"
        else:
            return "The character managed to observe their thoughts without getting lost in them. What does the idea of 'thoughts are not facts' mean to you?"
    
    return "What is one key message or feeling you are taking away from this scene?" # Fallback question

def display_story_scene(pdata, primary_theme_map, neutral_scenes):
    """
    Handles the generation and paragraph-by-paragraph display of the story scene.
    """
    scene_index = st.session_state.current_scene_index
    scene_info = st.session_state.scene_map[scene_index]
    scene_number = scene_info['number']
    scene_type = scene_info['type']
    
    st.header(f"Scene {scene_index + 1} / {st.session_state.total_scenes}")
    st.divider()

    # --- Text Generation and Retrieval ---
    full_text = None
    if scene_type == 'neutral':
        full_text = neutral_scenes.get(scene_number, "Neutral scene text not found.")
    else: 
        if st.session_state.story_text.get(scene_number) is None:
            with st.spinner("✍️ Crafting the next part of your story..."):
                new_text = None
                if scene_type == 'compassion':
                    new_text = generate_story_text(scene_number, st.session_state.ongoing_story, pdata, primary_theme_map)
                elif scene_type == 'kinder':
                    prev_compassion_scene_num = scene_number - 1
                    prev_text = st.session_state.story_text.get(prev_compassion_scene_num)
                    theme_name, _ = primary_theme_map[prev_compassion_scene_num]
                    new_text = generate_kinder_monologue_text(prev_text, theme_name, pdata)
                
                st.session_state.story_text[scene_number] = new_text or "GENERATION_FAILED"
                st.rerun()
        
        full_text = st.session_state.story_text.get(scene_number)

    if not full_text or full_text == "GENERATION_FAILED":
        st.error("Could not display the story. Please try refreshing.")
        return

    # --- Appending to ongoing story ---
    if scene_number not in st.session_state.appended_scenes:
        st.session_state.ongoing_story += "\n\n" + full_text
        st.session_state.appended_scenes.add(scene_number)
        
    # Display story and check if all paragraphs are shown
    all_paras_shown = display_paragraph_by_paragraph(scene_number, full_text)

    # If the last paragraph has been shown, display a button to move to reflections
    if all_paras_shown:
        st.divider()
        if st.button("Proceed to Reflection 🤔", key=f"reflect_btn_{scene_number}"):
            st.session_state.view_mode = 'reflection'
            st.rerun()

def display_reflection_page(pdata, primary_theme_map, scores, go_to_next_page):
    """
    Handles displaying the dynamic reflection questions for the current scene.
    """
    scene_index = st.session_state.current_scene_index
    scene_info = st.session_state.scene_map[scene_index]
    scene_number = scene_info['number']
    scene_type = scene_info['type']

    st.header(f"Reflection for Scene {scene_index + 1}")
    st.markdown("Take a moment to reflect on the scene you just read.")
    st.divider()

    # --- Q1: Relatedness ---
    if scene_type in ['compassion', 'kinder']:
        st.session_state.reflections[f"reflect_{scene_number}_relatedness"] = st.slider(
            "**How much did you relate to the main character in this scene?**",
            min_value=1, max_value=10, value=5,
            help="1 = Not at all, 10 = Completely"
        )

    # --- Q2: Valence ---
    st.session_state.reflections[f"reflect_{scene_number}_valence"] = st.radio(
        "**How pleasant or unpleasant did the scene make you feel?** (Valence)",
        options=['Very Unpleasant', 'Unpleasant', 'Neutral', 'Pleasant', 'Very Pleasant'],
        index=2, horizontal=True
    )

    # --- Q3: Arousal ---
    st.session_state.reflections[f"reflect_{scene_number}_arousal"] = st.radio(
        "**How much energy or calmness did you feel from the scene?** (Arousal)",
        options=['Very Low Energy ', 'Low Energy', 'Neutral', 'High Energy', 'Very High Energy'],
        index=2, horizontal=True
    )

    # --- Q4: Dynamic Question for Generated Scenes ---
    if scene_type in ['compassion', 'kinder']:
        theme_name, _ = primary_theme_map[scene_number]
        # This maps the theme to the correct score name
        score_key_map = { 
            "Self-Kindness vs Self-Judgment": "Self-Kindness vs Self-Judgment",
            "Common Humanity vs Isolation": "Common Humanity vs Isolation",
            "Mindfulness vs Overidentification": "Mindfulness vs Overidentification"
        }
        score_key = score_key_map.get(theme_name)
        user_score = scores.get(score_key, 50) # Default score if not found
        
        dynamic_question = generate_dynamic_fourth_question(theme_name, user_score)
        st.session_state.reflections[f"reflect_{scene_number}_dynamic"] = st.text_area(
            f"**{dynamic_question}**"
        )
    
    st.divider()

    # Button to move to the next scene
    if st.button("Continue to Next Scene ➡️", key=f"next_scene_btn_{scene_index}"):
        if scene_index < st.session_state.total_scenes - 1:
            st.session_state.current_scene_index += 1
            st.session_state.view_mode = 'story' # Switch back to story view for the next scene
            st.rerun()
        else:
            st.success("🎉 You have completed your personalized narrative journey!")
            # Optional: Add a small delay before navigating away
            go_to_next_page()
            st.rerun()


# --- ✅ 4. MODIFIED MAIN RENDER FUNCTION ---
def render(go_to_next_page):
    if "sc_scores" not in st.session_state or "personal_data" not in st.session_state:
        st.warning("⚠️ Required data not found. Please start from the beginning.")
        if st.button("Go to Start"): st.session_state.page = "start"; st.rerun()
        st.stop()

    st.title("📖 Your Personalized Narrative Journey")

    scores = st.session_state.sc_scores
    pdata = st.session_state.personal_data


    # --- Define Static Content for this page ---
    neutral_scenes = {
        1: """The office was quiet except for the low hum of the central air system. Rows of cubicles stretched evenly across the floor, separated by short partitions in a uniform gray tone. Fluorescent lights overhead provided even illumination without shadows. A digital clock above the doorway read 11:42 AM. Near the corner of the room, a large multifunction printer sat beside a recycling bin filled with discarded paper. 
        Its display screen showed a ready status. A person approached, inserted a badge into the reader, and selected a document from the queue. The machine started printing with a mechanical rhythm. Sheets of paper slid out one by one and settled on the output tray. 
        The person stood still, looking out the window while waiting. Outside, a construction crane moved slowly in the distance, rotating without sound through the sealed glass. Once the last page was printed, the person gathered the papers, aligned the stack, and returned to their desk.No one else spoke, and the room remained still apart from the distant tapping of keyboards. A wall calendar displayed the current month with no markings or annotations.
        """,
        
        4: """The automatic glass doors opened with a soft whoosh as a shopper entered the grocery store. The temperature inside was cool and regulated. Rows of fluorescent lights stretched across the ceiling, illuminating every aisle with a consistent brightness. The carts were neatly nested at the entrance. The shopper took a cart and moved toward the produce section. 
        Apples were stacked in even pyramids, misted at regular intervals by a quiet spray system. A sign above them read “Rs. 50/kg”. They picked up a plastic bag, selected four apples of similar size, and placed them inside. Then they proceeded to the bread aisle. Shelves were lined with loaves sorted by brand and type: whole wheat, white, rye, and multigrain. 
        They took one loaf from the middle shelf and placed it in the cart. At the far end of the aisle, another shopper turned the corner pushing a half-full cart. Neither acknowledged the other. Eventually, the shopper moved to the self-checkout area. The machine gave voice instructions in a neutral tone as each item was scanned and bagged. After payment was made, the shopper walked out carrying two filled bags, the doors sliding open again automatically.
        """,
        
        7: """A long, empty platform stretched beside two sets of train tracks. Overhead, a digital sign displayed the schedule: the next train was due in eight minutes. The platform surface was clean, with a yellow safety line painted along the edge. The air was still. A few people stood spaced apart, facing the tracks. One person leaned slightly against a pillar, scrolling through a phone.
        Another adjusted their backpack and looked briefly at the timetable. A recorded announcement played through overhead speakers, repeating information about train arrivals and platform safety. Far down the track, a distant rumble signaled an approaching train. The headlights became visible as it rounded a curve. People adjusted their positions slightly, but no one spoke. The train slowed to a stop with a hiss of air brakes, doors aligning exactly with the marked boarding areas.
        The passengers stepped in calmly. As the doors closed, the train pulled away with a soft whine. The platform was still again, and the digital sign reset to show the schedule for the next train.
        """ 
        }
    # neutral_question = "Did this scene evoke any particular feelings or thoughts for you? If so, please share them below." # Add a likert in neutral question- 5- point likert low neutral and high 
    
    # # valence and arousal questions 
    
    # static_reflective_questions = {
    #     2: ("How much do you relate to the main character? (On a scale of 1-10, with 10 being you relate completely)", "Do they deserve understanding or support? Why?"),
    #     3: ("Notice the shift in the character's inner voice. How did that feel?", "Can you identify a 'critic' and a 'compassionate' voice in your own thoughts?"),
    #     4: ("How much do you relate to the character in this scene?(On a scale of 1-10, with 10 being you relate completely)", "Do they deserve understanding or support? Why?"),
    #     5: ("How much do you relate to the character in this scene?(On a scale of 1-10, with 10 being you relate completely)", "Do they deserve understanding or support? Why?"),
    #     6: ("How does the new perspective change their view of others?", "What's a small way you could connect with someone tomorrow?"),
    #     8: ("How much do you relate to the character in this scene?(On a scale of 1-10, with 10 being you relate completely)", "Do they deserve understanding or support? Why?"),
    #     9: ("How did the character create distance from their overwhelming thoughts?", "What is one 'leaf' (a difficult thought) you could just watch float by?"),
    # }
    # assymetry in all 3 bands 
    #Aw index 
    #Efforrt index 
    #TF ANALYSLIS 
    #ERSP
    
    # Define theme mappings
    themes = [
        ("Self-Kindness vs Self-Judgment", get_kindness_story(scores.get("Self-Kindness vs Self-Judgment", 0))),
        ("Common Humanity vs Isolation", get_humanity_story(scores.get("Common Humanity vs Isolation", 0))),
        ("Mindfulness vs Overidentification", get_mindfulness_story(scores.get("Mindfulness vs Overidentification", 0))),
    ]
    primary_theme_map = {2: themes[0], 5: themes[1], 8: themes[2]}
    
    # --- Execute the story flow ---
    initialize_story_flow(scores)

    # Use the view_mode state to decide what to show
    if st.session_state.view_mode == 'story':
        display_story_scene(pdata, primary_theme_map, neutral_scenes)
    elif st.session_state.view_mode == 'reflection':
        display_reflection_page(pdata, primary_theme_map, scores, go_to_next_page)

