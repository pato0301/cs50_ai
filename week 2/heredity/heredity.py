import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    
    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    
    # Loop over all sets of people who might have the trait
    names = set(people)

    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    prob = 1
    for person in people:
        # Get number of genes and the trait probability
        num_gene = number_genes(people,one_gene,two_genes,person)
        prob_trait, bool_trait = get_trait(person,have_trait,num_gene)

        # Probability for persons without parents
        if people[person]['mother'] == None and people[person]['father'] == None:
            p_temp = PROBS["gene"][num_gene] * prob_trait
            prob *= p_temp
        # Probability for persons with parents
        else:
            # Get parents number of genes
            father = people[person]['father']
            mother = people[person]['mother']
            num_genes_father = number_genes(people,one_gene,two_genes,father)
            num_genes_mother = number_genes(people,one_gene,two_genes,mother)

            # Get child probability
            prob_of_child = 0
            for x in range(num_gene + 1):
                # You can only get 0 or 1 gene for your ancestor 
                # so when you have num_gene = 2 then x will be 0, 1 and 2. 
                # In that case when x=2, no probability should be computed.
                y = num_gene - x
                if x < 2 and y < 2:
                    prob_of_child += (prob_child(num_genes_mother,x) * prob_child(num_genes_father,y))

            prob_of_child *= prob_trait
            
            # final probability
            prob *= prob_of_child
        
        

    return prob

    # raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:
        # Get number of genes and if it has trait or not
        num_gene = number_genes(probabilities,one_gene,two_genes,person)
        prob_trait, bool_trait = get_trait(person,have_trait,num_gene)

        # Update probabilities for person gene and trait
        probabilities[person]['gene'][num_gene] += p
        probabilities[person]['trait'][bool_trait] += p

    # raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:

        total_gene = 0
        total_trait = 0  

        for i in probabilities[person]["gene"]:
            total_gene += probabilities[person]['gene'][i]
        
        for j in probabilities[person]["trait"]:
            total_trait += probabilities[person]['trait'][j]

        for gene in probabilities[person]['gene']:
            probabilities[person]['gene'][gene] /= total_gene
        
        for trait in probabilities[person]['trait']:
            probabilities[person]['trait'][trait] /= total_trait
    # raise NotImplementedError


def number_genes(people, one_gene, two_genes, person):
    """ 
    Get the number of genes for each person
    """
    zero_gene = set(people.keys()) - one_gene - two_genes
    if person in zero_gene:
        return 0
    elif person in one_gene:
        return 1
    else:
        return 2

def get_trait(person,have_trait,num_gene):
    if person in have_trait:
        return PROBS["trait"][num_gene][True], True
    else:
        return PROBS["trait"][num_gene][False], False

def prob_child(parent_num_genes,child_num_genes):
    prob_mut = PROBS["mutation"]
    prob_not_mut = 1 - prob_mut
    if parent_num_genes == 0:
        if child_num_genes == 0:
            return prob_not_mut
        else:
            return prob_mut
    elif parent_num_genes == 1:
        # The probability that receive the good one and not to mutate, 
        # or the prob to get the bad one an that it mutates
        # we have 50% chance on receiving any of the two genes
        p_temp = 0.5 * prob_not_mut + 0.5 * prob_mut
        if child_num_genes == 0:
            return p_temp
        # probability of sending the bad one and not to mutate
        else:
            return 1 - p_temp
    elif parent_num_genes == 2:
        # if havs the two genes wrong, the any of it that send must mutate 
        # so that the child has 0 wrong genes
        if child_num_genes == 0:
            return prob_mut
        else:
            return prob_not_mut

if __name__ == "__main__":
    main()
