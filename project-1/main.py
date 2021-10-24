import sys
import os

from github import Github

from repository import Repository
from metrics import LicenseMetric, RampUpMetric, CorrectnessMetric, BusFactorMetric, ResponsivenessMetric
from score import Ranking 
from log import log

def clear_log_file():
    log_file = os.environ['LOG_FILE']
    with open(log_file, "w") as file:
        file.write("")

def create_list_of_repositories(file_name, github):
    # Accepts the file name that contains a list of repository urls. Creates a list of Repository 
    # objects from these urls and returns this list. 

    repositories = []
    with open(file_name, "r") as file:
        log.log_url_file_read(file_name)
        for line in file.readlines():
            if line[-1] == "\n":
                line = line[:-1]
            print(line)

            repo = Repository(line, github)
            repositories.append(repo)

    log.log_url_file_closed(file_name)
    log.log_repo_list_created(repositories)

    return repositories

def print_results(metrics, rankings):
    # Prints out the metric names, repository urls, repository total scores, and repository sub 
    # scores. The repositories are printed in order of their total score. 
    output_string = ""

    header = "URL"
    for metric in metrics:
        header += " " + metric.name
    output_string += header + "\n"

    for ranking in rankings:
        repo_line = ranking.repository.url + " " + str(ranking.score)
        for score in ranking.repository.scores:
            repo_line += " " + str(score)
        output_string += repo_line + "\n"

    return output_string

def find_rankings(metrics, repositories):
    for metric in metrics:
        sub_scores = metric.calculate_scores(repositories)
        for i, sub_score in enumerate(sub_scores):
            repositories[i].scores.append(sub_score)

    rankingObject = Ranking(metrics)
    rankings      = rankingObject.get_rankings(repositories)

    log.log_final_rankings(rankings)
    return rankings

def main():
    # Creates a github object used for interacting with GitHub. Creates a list of repositories
    # that will be analyzed, and a list of metrics that will be used to calculate the score. 
    # Iterates through each metric to calculate each sub score for each repository. Ranks the 
    # repositories based on the total score.
    
    clear_log_file()

    token  = os.environ["GITHUB_TOKEN"]
    github = Github(token)

    repositories = create_list_of_repositories(sys.argv[1], github)
    metrics      = [
        RampUpMetric        ("RAMP_UP_SCORE"              , .3),
        CorrectnessMetric   ("CORRECTNESS_SCORE"          , .4),
        BusFactorMetric     ("BUS_FACTOR_SCORE"           , .8),
        ResponsivenessMetric("RESPONSIVE_MAINTAINER_SCORE", .3),
        LicenseMetric       ("LICENSE_SCORE"              , .5)
    ]
    log.log_metrics_created(metrics)

    rankings      = find_rankings(metrics, repositories)
    output_string = print_results(metrics, rankings)

    print(output_string)

if __name__ == "__main__":
    main()