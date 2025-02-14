# Hackapizza Gan

This is our team solution for datapizza hackathon.

## Trace

Benvenuti e benvenute nel Ciclo Cosmico 789, dove l'umanità ha superato non solo i confini del proprio sistema solare, ma anche quelli delle dimensioni conosciute. In questo vasto intreccio di realtà e culture, la gastronomia si è evoluta in un'arte che trascende spazio e tempo.

Ristoranti di ogni tipo arricchiscono il tessuto stesso del multiverso: dai sushi bar di Pandora che servono prelibati sashimi di Magikarp e ravioli al Vaporeon, alle taverne di Tatooine dove l’Erba Pipa viene utilizzata per insaporire piatti prelibati, fino ai moderni locali dove lo Slurm compone salse dai sapori contrastanti - l'universo gastronomico è vasto e pieno di sorprese.

L'espansione galattica ha portato con sé nuove responsabilità. La Federazione Galattica monitora attentamente ogni ingrediente, tecnica di preparazione e certificazione necessaria per garantire che il cibo servito sia sicuro per tutte le specie senzienti. Gli chef devono destreggiarsi tra regolamenti complessi, gestire ingredienti esotici che esistono simultaneamente in più stati quantici e rispettare le restrizioni alimentari di centinaia di specie provenienti da ogni angolo del multiverso.

Nel cuore pulsante di questo arcipelago cosmico di sapori, si erge un elemento di proporzioni titaniche, un'entità che trascende la mera materialità culinaria: la Pizza Cosmica. Si narra che la sua mozzarella sia stata ricavata dalla Via Lattea stessa e che, per cuocerla, sia stato necessario il calore di tre soli. Nessuno conosce le sue origini e culti religiosi hanno fondato la loro fede attorno al suo mistero.

La vostra missione è sviluppare un assistente AI che aiuti i viaggiatori intergalattici a navigare in questo ricco panorama culinario.

Il sistema dovrà essere in grado di suggerire agli utenti piatti appropriati sulla base delle loro richieste:
- Interpretando domande in linguaggio naturale
- Gestendo query complesse che coinvolgono preferenze e restrizioni alimentari
- Elaborando informazioni provenienti da diverse fonti (menu, blog post, leggi galattiche e manuali di cucina)
- Verificando la conformità dei piatti con le normative vigenti

Inoltre, il vostro sistema dovrà:
- Utilizzare tecniche di Generative AI (RAG, Agenti AI) per processare e comprendere i documenti forniti
- Implementare un modulo software in grado di:
    - Ricevere in input una richiesta utente relativa a possibili piatti che corrispondono a criteri espressi in linguaggio naturale
    - Fornire in output una lista di piatti che rispettano tali criteri sulla base della documentazione fornita

Che la forza sia con voi.

## Setup

To set up the project with uv, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/hackapizza_gas.git
    cd hackapizza_gas
    ```

2. Install `uv` folowing the instructions [here](https://docs.astral.sh/uv/getting-started/installation/#installation-methods):

3. Set up dependencies using:
    ```bash
    uv sync
    ```
4. You can add and remove packages using `uv add` and `uv remove`

## Contributing

To contribute to this project, follow these steps:

1. Branch out from `dev` with a branch named `dev-yourusername`:
    ```bash
    git checkout -b dev-yourusername dev
    ```

2. Make your changes and commit them:
    ```bash
    git add .
    git commit -m "Description of your changes"
    ```

3. Push your branch to the repository:
    ```bash
    git push origin dev-yourusername
    ```

4. Open a pull request to the `dev` branch.

## TODO

- [x] datamodels - think about how to handle the situation 'ingredients or techinques' 
- [x] datamodels - add list of known values when applicable (restaurants, planets)
- [x] markdown - fix markdown files
- [x] restaurants - extract and process restaurant descriptions and licences
- [x] filters - on planets (handling of distances)
- [x] filters - on chef licences (galactic code)
- [x] filters - on groups of appartenence (galactic code)
- [x] filters - on techinque parent groups (obtain during postprocessing, otherwise it messes up technique extraction)
- [x] recipes - extract quantities for restriced ingredients
- [x] restaurants - explore blog posts
- [ ] sirius cosmo - extract filter from recipe and techinque groups
- [ ] filters - on techinques licences (2 questions, galactic code)
- [ ] filters - on restricted ingredients (2 questions)
- [ ] prompts - add words difficult to spell in prompts, list of restaurants
- [ ] prompts - few shot examples for difficult questions tyes (multiple and or, etc..)
