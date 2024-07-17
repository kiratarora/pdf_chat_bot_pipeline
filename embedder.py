from InstructorEmbedding import INSTRUCTOR

# This file is the implemnetation for the BaseEmbedding class to incorporate custom embeding

model = INSTRUCTOR('hkunlp/instructor-large')
sentence = "3D ActionSLAM: wearable person tracking in multi-floor environments"
instruction = "Represent the Science title:"
embeddings = model.encode([[instruction,sentence]])
print(embeddings)
