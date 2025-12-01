import os
import torch

def get_filenames(dir_path):
    paths = []
    for filename in os.listdir(dir_path):
        if filename.endswith(".txt"):
            paths.append(os.path.join(dir_path, filename))
    return paths

def read_samples(file_path):
    samples = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            samples.append(line.strip())
    return samples

# class that loads and keeps benign and malicious samples along with their embeddings
class SamplesManager():
    def __init__(self):
        # file paths (list of strings)
        self.paths_b = None
        self.paths_m = None
        # samples (list of list of strings)
        self.benign = None
        self.malicious = None
        # embeddings (list of list of tensors)
        self.embeds_b = None
        self.embeds_m = None

        self.read_benign()
        self.read_malicious()

    def read_benign(self, benign_path='samples/benign/'):
        self.benign = []
        self.paths_b = get_filenames(benign_path)
        for path in self.paths_b:
            self.benign.append(read_samples(path))
    
    def read_malicious(self, malicious_path='samples/malicious/'):
        self.malicious = []
        self.paths_m = get_filenames(malicious_path)
        for path in self.paths_m:
            self.malicious.append(read_samples(path))
    
    def embed_samples(self, embed_fn):
        self.embeds_b = []
        for s in self.benign:
            self.embeds_b.append(embed_fn(s))

        self.embeds_m = []
        for s in self.malicious:
            self.embeds_m.append(embed_fn(s))

    def get_similarities(self, embed_input):
        sim_b_avg = []
        sim_m_avg = []
        out_text = ""

        out_text += 'Similarities with Benign / Malicious Samples:\n'
        out_text += '--------------------------------------------------------------------------\n'
        out_text += 'No.\t| Average Similarity\t| Path\n'
        out_text += '--------------------------------------------------------------------------\n'

        for i in range(len(self.embeds_b)):
            sim_avg = 0.0
            set_i = self.embeds_b[i]
            for emb in set_i:
                sim_avg += torch.nn.functional.cosine_similarity(embed_input, emb).item()
            sim_avg /= len(set_i)
            sim_b_avg.append(sim_avg)

            out_text += f'{i+1}\t| {sim_avg:.4f}\t\t| {self.paths_b[i]}\n'
        
        for i in range(len(self.embeds_m)):
            sim_avg = 0.0
            set_i = self.embeds_m[i]
            for emb in set_i:
                sim_avg += torch.nn.functional.cosine_similarity(embed_input, emb).item()
            sim_avg /= len(set_i)
            sim_m_avg.append(sim_avg)

            out_text += f'{i+1}\t| {sim_avg:.4f}\t\t| {self.paths_m[i]}\n'
                
        return sim_b_avg, sim_m_avg, out_text