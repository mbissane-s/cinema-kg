import pandas as pd
import re

df = pd.read_csv("../data/crawled_movies.csv")


def clean_name(text):
    if not isinstance(text, str):
        return text
    text = text.strip()
    # remove disambiguation suffixes like "(actor)", "(director)", "(film)"
    text = re.sub(r"\s*\(actor\)|\s*\(director\)|\s*\(actress\)", "", text, flags=re.IGNORECASE)
    # normalize multiple spaces
    text = re.sub(r"\s+", " ", text)
    # strip trailing punctuation
    text = text.strip(".,;:")
    return text


def tag_entity(text, column):
    if not isinstance(text, str):
        return None
    text = clean_name(text)
    if column == "film":
        return ("FILM", text)
    elif column == "director":
        return ("PERSON", text)
    elif column == "actor":
        return ("PERSON", text)
    return (None, text)


def is_valid_person(name):
    if not isinstance(name, str) or len(name) < 3:
        return False
    # reject entries that look like production company names or noise
    noise_patterns = [
        r"^\d+",
        r"^(and|with|also|see|the|a|an)\b",
        r"productions?$",
        r"studios?$",
        r"entertainment$",
        r"pictures?$",
        r"films?$",
    ]
    for pat in noise_patterns:
        if re.search(pat, name, re.IGNORECASE):
            return False
    return True


entities = []

for _, row in df.iterrows():
    film_tag = tag_entity(row["film"], "film")
    dir_tag  = tag_entity(row["director"], "director")
    act_tag  = tag_entity(row["actor"], "actor")

    if film_tag and dir_tag and act_tag:
        film_label = film_tag[1]
        dir_label  = dir_tag[1]
        act_label  = act_tag[1]

        if is_valid_person(dir_label) and is_valid_person(act_label):
            entities.append({
                "film":          film_label,
                "film_type":     film_tag[0],
                "director":      dir_label,
                "director_type": dir_tag[0],
                "actor":         act_label,
                "actor_type":    act_tag[0],
            })

result = pd.DataFrame(entities).drop_duplicates()
result.to_csv("../data/crawled_movies_clean.csv", index=False)

print(f"Entities extracted: {len(result)}")
print(result.head(10).to_string(index=False))

# ambiguity report
ambiguous = df[df["actor"].str.contains(r"\(actor\)|\(actress\)", na=False, regex=True)]
print(f"\nAmbiguous actor names resolved: {len(ambiguous)}")
print(ambiguous["actor"].head(5).tolist())
