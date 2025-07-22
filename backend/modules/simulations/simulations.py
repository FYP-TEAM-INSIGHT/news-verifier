from sinling import SinhalaTokenizer
from fastapi import HTTPException

tokenizer = SinhalaTokenizer()


demo_cases = [
    {
        "keyword": ["ඇන්ජලෝ", "මැතිව්ස්", "ටෙස්ට්", "ක්‍රිකට්", "සමුගැනීම"],
        "rumor_content": "ඇන්ජලෝ මැතිව්ස් ටෙස්ට් ක්‍රිකට් වලින් අහක් වෙනවලු 🥲 #SLCRICKET",
        "result": {
            "final_score": 0.93,
            "result": "NOT FAKE ✅",
            "semantic_ranking": [
                {
                    "score": 0.98,
                    "title": "හිටපු ශ්‍රී ලංකා නායක ඇන්ජලෝ මැතිව්ස් ටෙස්ට් ක්‍රිකට් පිටියට සමු දෙන බවට නිවේදනය කරයි....",
                    "url": "https://sinhala.newsfirst.lk/2025/05/23/%e0%b7%84%e0%b7%92%e0%b6%a7%e0%b6%b4%e0%b7%94-%e0%b7%81%e0%b7%8a%e2%80%8d%e0%b6%bb%e0%b7%93-%e0%b6%bd%e0%b6%82%e0%b6%9a%e0%b7%8f-%e0%b6%b1%e0%b7%8f",
                    "source": "News First",
                },
                {
                    "score": 0.75,
                    "title": "විරාත් කෝලි ටෙස්ට් ක්‍රිකට් පිටියෙන් සමුගැනීමට තීරණය කරයි..",
                    "url": "https://sinhala.newsfirst.lk/2025/05/10/%e0%b7%80%e0%b7%92%e0%b6%bb%e0%b7%8f%e0%b6%ad%e0%b7%8a-%e0%b6%9a%e0%b7%9d%e0%b6%bd%e0%b7%92-%e0%b6%a7%e0%b7%99%e0%b7%83%e0%b7%8a%e0%b6%a7%e0%b7%8a-%e0%b6%9a",
                    "source": "News First",
                },
            ],
            "breakdown": {
                "entity_similarity": 0.93,
                "semantic_similarity": 0.87,
                "source_credibility": 0.95,
                "per_entity": {
                    "persons": 0.98,
                    "locations": 0.8,
                    "events": 0.95,
                    "organizations": 0,
                },
            },
        },
    },
    {
        "keyword": ["ඇන්ජලෝ", "මැතිව්ස්", "එක්දින", "ක්‍රිකට්", "සමුගැනීම"],
        "rumor_content": "ඇන්ජලෝ මැතිව්ස් එක්දින ක්‍රිකට් වලින් අහක් වෙනවලු 🥲 #SLCRICKET",
        "result": {
            "final_score": 0.45,
            "result": "MIGHT BE FAKE ⚠️",
            "semantic_ranking": [
                {
                    "score": 0.62,
                    "title": "හිටපු ශ්‍රී ලංකා නායක ඇන්ජලෝ මැතිව්ස් ටෙස්ට් ක්‍රිකට් පිටියට සමු දෙන බවට නිවේදනය කරයි....",
                    "url": "https://sinhala.newsfirst.lk/2025/05/23/%e0%b7%84%e0%b7%92%e0%b6%a7%e0%b6%b4%e0%b7%94-%e0%b7%81%e0%b7%8a%e2%80%8d%e0%b6%bb%e0%b7%93-%e0%b6%bd%e0%b6%82%e0%b6%9a%e0%b7%8f-%e0%b6%b1%e0%b7%8f",
                    "source": "News First",
                },
                {
                    "score": 0.55,
                    "title": "විරාත් කෝලි ටෙස්ට් ක්‍රිකට් පිටියෙන් සමුගැනීමට තීරණය කරයි..",
                    "url": "https://sinhala.newsfirst.lk/2025/05/10/%e0%b7%80%e0%b7%92%e0%b6%bb%e0%b7%8f%e0%b6%ad%e0%b7%8a-%e0%b6%9a%e0%b7%9d%e0%b6%bd%e0%b7%92-%e0%b6%a7%e0%b7%99%e0%b7%83%e0%b7%8a%e0%b6%a7%e0%b7%8a-%e0%b6%9a",
                    "source": "News First",
                },
                {
                    "score": 0.48,
                    "title": "කිසිදු ශතකයක් නොමැතිව එංගලන්තයෙන් ලකුණු 400ක්",
                    "url": "https://sinhala.newsfirst.lk/2025/05/29/%e0%b6%9a%e0%b7%92%e0%b7%83%e0%b7%92%e0%b6%af%e0%b7%94-%e0%b7%81%e0%b6%ad%e0%b6%9a%e0%b7%9a%e0%b6%9a%e0%b7%8a-%e0%b7%80%e0%b7%8f%e0%b6%bb%e0%b7%8a%e0%b6%ad%e0%b7%8f-%e0%b6%b1%e0%b7%9c%e0%b6%9a%e0%b6%bb-%e0%b6%89%e0%b6%b1%e0%b7%92%e0%b6%b8%e0%b7%9a-%e0%b6%ad%e0%b7%94%e0%b7%85",
                    "source": "News First",
                },
            ],
            "breakdown": {
                "entity_similarity": 0.60,
                "semantic_similarity": 0.40,
                "source_credibility": 0.95,
                "per_entity": {
                    "persons": 0.98,
                    "locations": 0.8,
                    "events": 0.2,
                    "organizations": 0,
                },
            },
        },
    },
    {
        "keyword": ["ට්‍රම්ප්", "ඊශ්‍රායලය", "ඉරානය", "ප්‍රහාර", "නැහැ", "සටන් විරාමය"],
        "rumor_content": "ට්‍රම්ප් කියනවා ඊශ්‍රායලය ඉරානයට පහර දෙන්නේ නෑ, සටන් විරාමයලු දැන් ක්‍රියාත්මක! #ලෝකදේශපාලනය",
        "result": {
            "final_score": 0.88,
            "result": "NOT FAKE ✅",
            "semantic_ranking": [
                {
                    "score": 0.96,
                    "title": "ඊශ්‍රායලය ඉරානයට පහර දෙන්නේ නැහැ; සටන් විරාමය ක්‍රියාත්මකයි! - ට්‍රම්ප්",
                    "url": "https://hirunews.lk/408207/israel-is-not-attacking-iran-ceasefire-is-in-effect-trump",
                    "source": "hirunews",
                },
                {
                    "score": 0.85,
                    "title": "සටන් විරාමය ආරම්භ වීමෙන් පසු ඊශ්‍රායලයට මිසයිලයක් එල්ල කළ බවට වන චෝදනා ඉරානය ප්‍රතික්ෂේප කරයි",
                    "url": "https://hirunews.lk/408173/iran-denies-firing-missile-at-israel-after-ceasefire-begins",
                    "source": "hirunews",
                },
                {
                    "score": 0.70,
                    "title": "ඉරාන න්‍යෂ්ටික බලාගාරවලට එල්ල වූ අමෙරිකානු සහ ඊශ්‍රායල ප්‍රහාර හෙළා දකිමින් ඉරානයට රුසියාවේ සහාය",
                    "url": "https://hirunews.lk/408191/russia-supports-iran-condemns-us-and-israeli-attacks-on-iranian-nuclear-facilities",
                    "source": "hirunews",
                },
            ],
            "breakdown": {
                "entity_similarity": 0.90,
                "semantic_similarity": 0.85,
                "source_credibility": 0.90,
                "per_entity": {
                    "persons": 0.95,
                    "locations": 0.90,
                    "events": 0.90,
                    "organizations": 0.8,
                },
            },
        },
    },
    {
        "keyword": ["ඊශ්‍රායලය", "ඉරානය", "ඔත්තු බැලීම", "අත්අඩංගුවට", "1000ක්"],
        "rumor_content": "ඉරානය ඊශ්‍රායලයට ඔත්තු බැලූ 1000කට වඩා අත්අඩංගුවට ගත්තා කියල ආරංචියක් #MiddleEast",
        "result": {
            "final_score": 0.65,
            "result": "MIGHT BE FAKE ⚠️",
            "semantic_ranking": [
                {
                    "score": 0.80,
                    "title": "ඊශ්‍රායලයට ඔත්තු බැලූ 700ක් ඉරාන අත්අඩංගුවට",
                    "url": "https://hirunews.lk/408360/iran-arrests-700-people-for-spying-for-israel",
                    "source": "hirunews",
                },
                {
                    "score": 0.50,
                    "title": "ඉරාන න්‍යෂ්ටික බලාගාරවලට එල්ල වූ අමෙරිකානු සහ ඊශ්‍රායල ප්‍රහාර හෙළා දකිමින් ඉරානයට රුසියාවේ සහාය",
                    "url": "https://hirunews.lk/408191/russia-supports-iran-condemns-us-and-israeli-attacks-on-iranian-nuclear-facilities",
                    "source": "hirunews",
                },
                {
                    "score": 0.45,
                    "title": "සටන් විරාමය ආරම්භ වීමෙන් පසු ඊශ්‍රායලයට මිසයිලයක් එල්ල කළ බවට වන චෝදනා ඉරානය ප්‍රතික්ෂේප කරයි",
                    "url": "https://hirunews.lk/408173/iran-denies-firing-missile-at-israel-after-ceasefire-begins",
                    "source": "hirunews",
                },
            ],
            "breakdown": {
                "entity_similarity": 0.70,
                "semantic_similarity": 0.60,
                "source_credibility": 0.90,
                "per_entity": {
                    "persons": 0,
                    "locations": 0.95,
                    "events": 0.7,
                    "organizations": 0,
                },
            },
        },
    },
    {
        "keyword": ["මහින්දානන්ද", "අලුත්ගමගේ", "වසර", "30", "සිරදඬුවම්", "කැරම් බෝඩ්"],
        "rumor_content": "මහින්දානන්ද අලුත්ගමගේට කැරම් බෝඩ් ගනුදෙනුවට වසර 30ක සිරදඬුවම් දීලලු! #ප්‍රවෘත්ති",
        "result": {
            "final_score": 0.60,
            "result": "MIGHT BE FAKE ⚠️",
            "semantic_ranking": [
                {
                    "score": 0.85,
                    "title": "කැරම් බෝඩ් ගණුදෙණුවට හිටපු අමාත්‍යවරුන් වන මහින්දානන්දට සහ නලීන් ප්‍රනාන්දුට බරපතල වැඩ සහිත සිරදඬුවම්.",
                    "url": "https://sinhala.newsfirst.lk/2025/05/29/%e0%b6%9a%e0%b7%90%e0%b6%bb%e0%b6%b8%e0%b7%8a-%e0%b6%b6%e0%b7%9c%e0%b6%a9%e0%b7%8a-%e0%b6%9c%e0%b6%ab%e0%b7%94%e0%b6%af%e0%b7%99%e0%b6%ab%e0%b7%94%e0%b7%80%e0%b6%a7",
                    "source": "News First",
                },
                {
                    "score": 0.60,
                    "title": "මර්වින් සහ ප්‍රසන්න රණවීර යළි රිමාන්ඩ්...",
                    "url": "https://sinhala.newsfirst.lk/2025/05/20/%e0%b6%b8%e0%b6%bb%e0%b7%8a%e0%b7%80%e0%b7%92%e0%b6%b1%e0%b7%8a-%e0%b7%83%e0%b7%84-%e0%b6%b4%e0%b7%8a%e2%80%8d%e0%b6%bb%e0%b7%83%e0%b6%b1%e0%b7%8a%e0%b6%b1",
                    "source": "News First",
                },
                {
                    "score": 0.55,
                    "title": "හිටපු ඇමති දුමින්ද යළි රිමාන්ඩ්.",
                    "url": "https://sinhala.newsfirst.lk/2025/05/29/%e0%b7%84%e0%b7%92%e0%b6%a7%e0%b6%b4%e0%b7%94-%e0%b6%87%e0%b6%b8%e0%b6%ad%e0%b7%92-%e0%b6%af%e0%b7%94%e0%b6%b8%e0%b7%92%e0%b6%b1%e0%b7%8a%e0%b6%af-%e0%b6%ba",
                    "source": "News First",
                },
            ],
            "breakdown": {
                "entity_similarity": 0.75,
                "semantic_similarity": 0.50,
                "source_credibility": 0.95,
                "per_entity": {
                    "persons": 0.9,
                    "locations": 0,
                    "events": 0.6,
                    "organizations": 0,
                },
            },
        },
    },
    {
        "keyword": ["හාවඩ්", "විශ්වවිද්‍යාලය", "අත්හිටුවයි", "ශ්‍රී ලංකා", "සිසුන්"],
        "rumor_content": "හාවඩ් විශ්වවිද්‍යාලය ශ්‍රී ලංකා සිසුන් ඇතුළත් කර ගැනීම අත්හිටුවයි! #අධ්‍යාපනය",
        "result": {
            "final_score": 0.35,
            "result": "POSSIBLY FAKE ❌",
            "semantic_ranking": [
                {
                    "score": 0.40,
                    "title": "හාවඩ් විශ්වවිද්‍යාලයට විදේශීය සිසුන් ඇතුළත් කර ගැනීම අත්හිටුවයි",
                    "url": "https://sinhala.newsfirst.lk/2025/05/23/%e0%b7%84%e0%b7%8f%e0%b7%80%e0%b6%a9%e0%b7%8a-%e0%b7%80%e0%b7%92%e0%b7%81%e0%b7%8a%e0%b7%80%e0%b7%80%e0%b7%92%e0%b6%af%e0%b7%8a%e2%80%8d%e0%b6%ba%e0%b7%8f%e0%b6%bd%e0%b6%ba",
                    "source": "News First",
                },
                {
                    "score": 0.30,
                    "title": "නවකවදය ඇතුළු සියලු ආකාරයේ හිංසනයන් වැළැක්වීම සඳහා කාර්යසාධක බළකායක්",
                    "url": "https://sinhala.newsfirst.lk/2025/06/25/%e0%b6%b1%e0%b7%80%e0%b6%9a%e0%b7%80%e0%b6%af%e0%b6%ba-%e0%b6%87%e0%b6%ad%e0%b7%94%e0%b7%85%e0%b7%94-%e0%b7%83%e0%b7%92%e0%b6%ba%e0%b6%bd%e0%b7%94-%e0%b6%86",
                    "source": "News First",
                },
                {
                    "score": 0.25,
                    "title": "නවක වදය චෝදනාවකට අග්නිදිග සරසවියේ සිසුන් 22 කුගේ පන්ති තහනම්.",
                    "url": "https://sinhala.newsfirst.lk/2025/06/25/%e0%b6%b1%e0%b7%80%e0%b6%9a-%e0%b7%80%e0%b6%af%e0%b6%ba-%e0%b6%a2%e0%b7%9d%e0%b6%af%e0%b6%b1%e0%b7%8f%e0%b7%80%e0%b6%9a%e0%b6%a7-%e0%b6%8 අග්",
                    "source": "News First",
                },
            ],
            "breakdown": {
                "entity_similarity": 0.40,
                "semantic_similarity": 0.30,
                "source_credibility": 0.95,
                "per_entity": {
                    "persons": 0,
                    "locations": 0.5,
                    "events": 0.2,
                    "organizations": 0.7,
                },
            },
        },
    },
    {
        "keyword": ["චමරි", "අතපත්තු", "පළමු", "ස්ථානය", "ක්‍රිකට්", "එක්දින"],
        "rumor_content": "චමරි අතපත්තු එක්දින ක්‍රිකට් ශ්‍රේණිගත කිරීම්වල පළමු තැනට ඇවිල්ලලු! 💪🏏",
        "result": {
            "final_score": 0.55,
            "result": "MIGHT BE FAKE ⚠️",
            "semantic_ranking": [
                {
                    "score": 0.70,
                    "title": "චමරි අතපත්තු එක්දින ක්‍රිකට් ශ්‍රේණිගත කිරීම්හි 7 වැනි තැනට...",
                    "url": "https://sinhala.newsfirst.lk/2025/05/14/%e0%b6%a0%e0%b6%b8%e0%b6%bb%e0%b7%92-%e0%b6%85%e0%b6%ad%e0%b6%b4%e0%b6%ad%e0%b7%8a%e0%b6%ad%e0%b7%94-%e0%b6%91%e0%b6%9a%e0%b7%8a%e0%b6%af%e0%b7%92%e0%b6%b1",
                    "source": "News First",
                },
                {
                    "score": 0.50,
                    "title": "2025 ICC එක්දින ක්‍රිකට් කණ්ඩායමේ නායකත්වය චරිත් අසලංකට",
                    "url": "https://sinhala.newsfirst.lk/2025/01/24/2024-icc-%e0%b6%91%e0%b6%9a%e0%b7%8a%e0%b6%af%e0%b7%92%e0%b6%b1-%e0%b6%9a%e0%b7%8a%e2%80%8d%e0%b6%bb",
                    "source": "News First",
                },
                {
                    "score": 0.45,
                    "title": "කිසිදු ශතකයක් නොමැතිව එංගලන්තයෙන් ලකුණු 400ක්",
                    "url": "https://sinhala.newsfirst.lk/2025/05/29/%e0%b6%9a%e0%b7%92%e0%b7%83%e0%b7%92%e0%b6%af%e0%b7%94-%e0%b7%81%e0%b6%ad%e0%b6%9a%e0%b7%9a%e0%b6%9a%e0%b7%8a-%e0%b7%80%e0%b7%8f%e0%b6%bb%e0%b7%8a%e0%b6%ad%e0%b7%8f-%e0%b6%b1%e0%b7%9c%e0%b6%9a%e0%b6%bb-%e0%b6%89%e0%b6%b1%e0%b7%92%e0%b6%b8%e0%b7%9a-%e0%b6%ad%e0%b7%94%e0%b7%85",
                    "source": "News First",
                },
            ],
            "breakdown": {
                "entity_similarity": 0.70,
                "semantic_similarity": 0.40,
                "source_credibility": 0.95,
                "per_entity": {
                    "persons": 0.98,
                    "locations": 0.8,
                    "events": 0.5,
                    "organizations": 0,
                },
            },
        },
    },
    {
        "keyword": ["කාලිංග", "කුමාරගේ", "ආසියානු", "මලල ක්‍රීඩා", "රන් පදක්කම", "මීටර 400"],
        "rumor_content": "ආසියානු මලල ක්‍රීඩා උළෙලේ මීටර 400න් කාලිංග කුමාරගේට රන් පදක්කමක්! 🥇🇱🇰",
        "result": {
            "final_score": 0.68,
            "result": "MIGHT BE FAKE ⚠️",
            "semantic_ranking": [
                {
                    "score": 0.85,
                    "title": "ආසියානු මලල ක්‍රීඩා උළෙලේ මීටර 400 පිරිමි ධාවන ඉවසව්වෙන් ශ්‍රී ලංකාවේ කාලිංග කුමාරගේ ලෝකඩ පදක්කම දිනාගනී...",
                    "url": "https://sinhala.newsfirst.lk/2025/05/28/%e0%b6%86%e0%b7%83%e0%b7%92%e0%b6%ba%e0%b7%8f%e0%b6%b1%e0%b7%94-%e0%b6%b8%e0%b6%bd%e0%b6%bd-%e0%b6%9a%e0%b7%8a%e2%80%8d%e0%b6%bb%e0%b7%93%e0%b6%a9%e0%b7%8f",
                    "source": "News First",
                },
                {
                    "score": 0.60,
                    "title": "අපේ ක්‍රීඩකයින් රිදියෙන් සැරසූ ආසියානු යොවුන් බොක්සින් තරගාවලිය....",
                    "url": "https://sinhala.newsfirst.lk/2025/05/23/%e0%b6%85%e0%b6%b4%e0%b7%9a-%e0%b6%9a%e0%b7%8a%e2%80%8d%e0%b6%bb%e0%b7%93%e0%b6%a9%e0%b6%9a%e0%b7%92%e0%b6%b1%e0%b7%8a-%e0%b6%bb%e0%b7%92%e0%b6%af%e0%b7%92",
                    "source": "News First",
                },
            ],
            "breakdown": {
                "entity_similarity": 0.80,
                "semantic_similarity": 0.65,
                "source_credibility": 0.95,
                "per_entity": {
                    "persons": 0.98,
                    "locations": 0.9,
                    "events": 0.6,
                    "organizations": 0,
                },
            },
        },
    },
    {
        "keyword": ["ශ්‍රීකාන්ත්", "නළු", "අත්අඩංගුවට", "ඉන්දියාව"],
        "rumor_content": "ඉන්දීය නළු ශ්‍රීකාන්ත් අත්අඩංගුවට ගත්තා කියන එක ඇත්තද? #Bollywood",
        "result": {
            "final_score": 0.90,
            "result": "NOT FAKE ✅",
            "semantic_ranking": [
                {
                    "score": 0.95,
                    "title": "ඉන්දීය නළු ශ්‍රීකාන්ත් අත්අඩංගුවට",
                    "url": "https://hirunews.lk/408198/indian-actor-srikanth-arrested",
                    "source": "hirunews",
                },
                {
                    "score": 0.60,
                    "title": "අමෙරිකානු නළු ජෝ මැරිනෙලි ජීවිතක්ෂයට",
                    "url": "https://hirunews.lk/408397/american-actor-joe-marinelli-passes-away",
                    "source": "hirunews",
                },
            ],
            "breakdown": {
                "entity_similarity": 0.90,
                "semantic_similarity": 0.85,
                "source_credibility": 0.90,
                "per_entity": {
                    "persons": 0.98,
                    "locations": 0.9,
                    "events": 0.8,
                    "organizations": 0,
                },
            },
        },
    },
    {
        "keyword": ["ජෝ", "මැරිනෙලි", "අමෙරිකානු", "නළු", "අසනීප"],
        "rumor_content": "අමෙරිකානු නළු ජෝ මැරිනෙලිට අසනීප වෙලා කියලා ආරංචියක්? #HollywoodNews",
        "result": {
            "final_score": 0.40,
            "result": "MIGHT BE FAKE ⚠️",
            "semantic_ranking": [
                {
                    "score": 0.75,
                    "title": "අමෙරිකානු නළු ජෝ මැරිනෙලි ජීවිතක්ෂයට",
                    "url": "https://hirunews.lk/408397/american-actor-joe-marinelli-passes-away",
                    "source": "hirunews",
                },
                {
                    "score": 0.50,
                    "title": "ඉන්දීය නළු ශ්‍රීකාන්ත් අත්අඩංගුවට",
                    "url": "https://hirunews.lk/408198/indian-actor-srikanth-arrested",
                    "source": "hirunews",
                },
            ],
            "breakdown": {
                "entity_similarity": 0.70,
                "semantic_similarity": 0.30,
                "source_credibility": 0.90,
                "per_entity": {
                    "persons": 0.98,
                    "locations": 0.9,
                    "events": 0.2,
                    "organizations": 0,
                },
            },
        },
    },
    {
        "keyword": ["කොළඹ", "බස්", "නැවතුම්පොළ", "වසර", "2", "නවීකරණය"],
        "rumor_content": "කොළඹ මධ්‍යම බස් නැවතුම්පොළ අවුරුදු 2කින් අලුත් කරනවලු! #LKA",
        "result": {
            "final_score": 0.60,
            "result": "MIGHT BE FAKE ⚠️",
            "semantic_ranking": [
                {
                    "score": 0.80,
                    "title": "ක්ලීන් ශ්‍රිලංකා වැඩසටහනට සමගාමීව කොළඹ මධ්‍යම බස් නැවතුම්පොළ නවීකරණය කිරීමට සැලසුම්..",
                    "url": "https://sinhala.newsfirst.lk/2025/06/24/clean-sri-lanka-%e0%b7%80%e0%b7%90%e0%b6%a9%e0%b7%83",
                    "source": "News First",
                }
            ],
            "breakdown": {
                "entity_similarity": 0.80,
                "semantic_similarity": 0.50,
                "source_credibility": 0.95,
                "per_entity": {
                    "persons": 0,
                    "locations": 0.9,
                    "events": 0.5,
                    "organizations": 0.8,
                },
            },
        },
    },
    {
        "keyword": ["නුවරඑළිය", "වෙසක්", "සැමරුම", "විශේෂ", "සතිය"],
        "rumor_content": "මේ වෙසක් සතියේ විශේෂ සැමරුමක් නුවරඑළියේ පැවැත්වෙනවා කියලා ආරංචියක්? #Vesak",
        "result": {
            "final_score": 0.90,
            "result": "NOT FAKE ✅",
            "semantic_ranking": [
                {
                    "score": 0.95,
                    "title": "රාජ්‍ය වෙසක් සැමරුම නුවරඑළියේදී ..",
                    "url": "https://sinhala.newsfirst.lk/2025/05/12/%e0%b6%bb%e0%b7%8f%e0%b6%a2%e0%b7%8a%e2%80%8d%e0%b6%ba-%e0%b7%80%e0%b7%99%e0%b7%83%e0%b6%9a%e0%b7%8a-%e0%b7%83%e0%b7%90%e0%b6%b8%e0%b6%bb%e0%b7%94%e0%b6%b8",
                    "source": "News First",
                }
            ],
            "breakdown": {
                "entity_similarity": 0.90,
                "semantic_similarity": 0.85,
                "source_credibility": 0.95,
                "per_entity": {
                    "persons": 0,
                    "locations": 0.98,
                    "events": 0.95,
                    "organizations": 0,
                },
            },
        },
    },
    {
        "keyword": ["ලෝක රූ රැජිණ", "ශ්‍රී ලංකාව", "අනුදි ගුණසේකර", "කිරුළ"],
        "rumor_content": "මේ පාර ලෝක රූ රැජිණ කිරුළ අනුදි ගුණසේකරටලු! ලංකාවට ආඩම්බරයක්! 👑🇱🇰",
        "result": {
            "final_score": 0.30,
            "result": "POSSIBLY FAKE ❌",
            "semantic_ranking": [
                {
                    "score": 0.60,
                    "title": "අනුදි ගුණසේකර ලෝක රූ රැජිණ අවසන් 40 වටයට සුදුසුකම් නොලබයි..",
                    "url": "https://sinhala.newsfirst.lk/2025/05/31/%e0%b6%85%e0%b6%b1%e0%b7%94%e0%b6%af%e0%b7%92-%e0%b6%9c%e0%b7%94%e0%b6%ab%e0%b7%83%e0%b7%9a%e0%b6%9a%e0%b6%bb-%e0%b6%bd%e0%b7%9d%e0%b6%9a-%e0%b6%bb%e0%b7%96",
                    "source": "News First",
                },
                {
                    "score": 0.55,
                    "title": "72 වැනි ලෝක රූ රැජින කිරුළ තායිලන්තයේ ඔපල් සුචාටාට",
                    "url": "https://sinhala.newsfirst.lk/2025/05/31/72-%e0%b7%80%e0%b7%90%e0%b6%b1%e0%b7%92-%e0%b6%bd%e0%b7%9d%e0%b6%9a-%e0%b6%bb%e0%b7%96-%e0%b6%bb%e0%b7%92%e0%b6%a2%e0%b7%92%e0%b6%b1",
                    "source": "News First",
                },
            ],
            "breakdown": {
                "entity_similarity": 0.50,
                "semantic_similarity": 0.20,
                "source_credibility": 0.95,
                "per_entity": {
                    "persons": 0.98,
                    "locations": 0.2,
                    "events": 0.1,
                    "organizations": 0,
                },
            },
        },
    },
    {
        "keyword": ["රාජ්‍ය සේවය", "බඳවා ගැනීම්", "ලක්ෂයක්"],
        "rumor_content": "රාජ්‍ය සේවයට අලුතින් ලක්ෂයක් බඳවා ගන්නවලු! ලොකු අවස්ථාවක්! #රැකියා",
        "result": {
            "final_score": 0.65,
            "result": "MIGHT BE FAKE ⚠️",
            "semantic_ranking": [
                {
                    "score": 0.80,
                    "title": "වසර 7 කට පසු රාජ්‍ය සේවයකට තිස් දහසක් බඳවා ගැනීම ඇරඹේයි - රාජ්‍ය පරිපාලන පළාත් සභා හා පළාත් පාලන අමාත්‍යංශය",
                    "url": "https://sinhala.newsfirst.lk/2025/06/25/%e0%b7%80%e0%b7%83%e0%b6%bb-7-%e0%b6%9a%e0%b6%a7-%e0%b6%b4%e0%b7%83%e0%b7%94-%e0%b6%bb%e0%b6%a2%e0%b7%8a%e2%80%8d%e0%b6%ba",
                    "source": "News First",
                }
            ],
            "breakdown": {
                "entity_similarity": 0.80,
                "semantic_similarity": 0.50,
                "source_credibility": 0.95,
                "per_entity": {
                    "persons": 0,
                    "locations": 0,
                    "events": 0.7,
                    "organizations": 0.9,
                },
            },
        },
    },
]


def simulate_news_verification(article_text: str):
    tokens = tokenizer.tokenize(article_text)
    max_match_count = 0
    best_case = None

    for case in demo_cases:
        match_count = sum(1 for keyword in case["keyword"] if keyword in tokens)
        if match_count > max_match_count:
            max_match_count = match_count
            best_case = case

    if best_case and max_match_count > 0:
        return best_case["result"]

    raise HTTPException(
        status_code=400, detail="No matched news found in verified database"
    )
