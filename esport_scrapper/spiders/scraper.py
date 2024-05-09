import scrapy
from scrapy import Selector
from scrapy.http import Response
from scrapy_selenium import SeleniumRequest


class EsportsSpider(scrapy.Spider):
    name = "esports"
    allowed_domains = ["escharts.com"]
    start_urls = ["https://escharts.com/"]
    download_delay = 3

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                screenshot=True,
                wait_time=5,
                callback=self.parse)
            self.logger.info(F"start request: {url}")

    def parse(self, response: Response, **kwargs):
        element = response.css(
            "div.w-full.overflow-hidden"
            ".border.lg\\:flex.border-card.rounded-b-xl"
            "> div.w-full.grid-cols-5.lg\\:grid"
        ).get()
        selector = Selector(text=element)
        yield {
            "Tournaments": f"{selector.css(
                "a:nth-child(1) div.font-bold::text"
            ).get()}",
            "Matches": f"{selector.css(
                "a:nth-child(2) div.font-bold::text"
            ).get()}",
            "Teams": f"{selector.css(
                "a:nth-child(3) div.font-bold::text"
            ).get()}",
            "Players": f"{selector.css(
                "a:nth-child(4) div.font-bold::text"
            ).get()}",
            "Games": f"{selector.css(
                "a:nth-child(5) div.font-bold::text"
            ).get()}",
            # "Upcoming matches": self.parse_upcoming_matches(response),
            "Live matches": self.parse_live_matches(response),
            "Top orgs": self.parse_top_organization(response),
        }

    def parse_upcoming_matches(self, response: Response, **kwargs):
        element = response.css(
            "#upcoming_matches_block div.-mx-6.py-3.-my-6"
        ).get()
        selector = Selector(text=element)
        matches_data = {}

        first_team = selector.css(
            "a:nth-child(1) div.flex.flex-wrap.items-center.flex-1 "
            "> div:nth-child(1) > span::text").get()
        second_team = selector.css(
            "a:nth-child(1) div.flex.flex-wrap.items-center.flex-1 "
            "> div:nth-child(3) > span::text").get()
        tournament = selector.css(
            "a:nth-child(2) span.leading-4::text").get().strip()
        match_date = selector.css(
            "a:nth-child(2) div.flex.items-center.w-full.gap-x-2 "
            "div:nth-child(3) div::text").get()

        if first_team and second_team and tournament and match_date:
            matches_data[
                "Match #1"
            ] = (f"{first_team} vs {second_team}, {tournament} "
                 f"{' '.join(match_date.strip().split())}")

        third_team = selector.css(
            "a:nth-child(2) div.flex.flex-wrap.items-center.flex-1 >"
            " div:nth-child(1) > span::text").get()
        fourth_team = selector.css(
            "a:nth-child(2) div.flex.flex-wrap.items-center.flex-1 >"
            " div:nth-child(3) > span::text").get()
        tournament_second = selector.css(
            "a:nth-child(2) span.leading-4::text").get().strip()
        match_date_second = selector.css(
            "a:nth-child(2) div.flex.items-center.w-full.gap-x-2 "
            "div:nth-child(3) div::text").get()

        if (
                third_team
                and fourth_team
                and tournament_second and match_date_second
        ):
            matches_data[
                "Match #2"
            ] = (f"{third_team} vs {fourth_team}, {tournament_second} "
                 f"{' '.join(match_date_second.strip().split())}")

        fifth_team = selector.css(
            "a:nth-child(3) div.flex.flex-wrap.items-center.flex-1 "
            "> div:nth-child(1) > span::text").get()
        sixth_team = selector.css(
            "a:nth-child(3) div.flex.flex-wrap.items-center.flex-1 "
            "> div:nth-child(3) > span::text").get()
        tournament_third = selector.css(
            "a:nth-child(3) span.leading-4::text").get().strip()
        match_date_third = selector.css(
            "a:nth-child(3) div.flex.items-center.w-full.gap-x-2 "
            "div:nth-child(3) div::text").get()

        if fifth_team and sixth_team and tournament_third and match_date_third:
            matches_data[
                "Match #3"
            ] = (f"{fifth_team} vs {sixth_team}, {tournament_third} "
                 f"{' '.join(match_date_third.strip().split())}")

        return matches_data

    def parse_live_matches(self, response: Response, **kwargs) -> dict:
        element = response.css(
            "#live_matches_block div.-mx-6.flex.flex-col.gap-y-1.-my-6 "
        ).get()
        selector = Selector(text=element)
        live_matches_data = {}
        try:
            first_match_team_one = selector.css(
                "a:nth-child(1) "
                "div.flex.flex-wrap.items-center.flex-1 "
                "> div:nth-child(3) > span::text"
            ).get()
            first_match_team_two = selector.css(
                "a:nth-child(1) "
                "div.flex.flex-wrap.items-center.flex-1 "
                "> div:nth-child(1) > span::text"
            ).get()
            first_match_tournament = selector.css(
                "a:nth-child(2) span.leading-4::text"
            ).get().strip()

            if (
                    first_match_team_one
                    and first_match_team_two
                    and first_match_tournament
            ):
                live_matches_data[
                    "First Match"
                ] = (f"{first_match_team_one} vs {first_match_team_two},"
                     f" {first_match_tournament})")
        except Exception as error:
            live_matches_data["First Match"] = "Match not found"
            self.logger.error(f"LIVE_MATCHES_ERROR: {error}")


        try:
            second_match_team_one = selector.css(
                "a:nth-child(2) "
                "div.flex.flex-wrap.items-center.flex-1 "
                "> div:nth-child(1) > span::text"
            ).get()
            second_match_team_two = selector.css(
                "a:nth-child(2) "
                "div.flex.flex-wrap.items-center.flex-1 "
                "> div:nth-child(3) > span::text"
            ).get()
            second_match_tournament = selector.css(
                "a:nth-child(2) span.leading-4::text"
            ).get().strip()

            if (
                    second_match_team_one
                    and second_match_team_two
                    and second_match_tournament
            ):
                live_matches_data[
                    "Second Match"
                ] = (f"{second_match_team_one} vs {second_match_team_two},"
                     f" {second_match_tournament})")

        except Exception as error:
            live_matches_data["Second Match"] = "Match not found"
            self.logger.error(F"LIVE_MATCHES_ERROR: {error}")

        try:
            third_match_team_one = selector.css(
                "a:nth-child(3) "
                "div.flex.flex-wrap.items-center.flex-1 "
                "> div:nth-child(1) > span::text"
            ).get()
            third_match_team_two = selector.css(
                "a:nth-child(3) "
                "div.flex.flex-wrap.items-center.flex-1 "
                "> div:nth-child(3) > span::text"
            ).get()
            third_match_tournament = selector.css(
                "a:nth-child(3) span.leading-4::text"
            ).get().strip()

            if (
                    third_match_team_one
                    and third_match_team_two
                    and third_match_tournament
            ):
                live_matches_data[
                    "Third Match"
                ] = (f"{third_match_team_one} vs {third_match_team_two},"
                     f" {third_match_tournament})")
        except Exception as error:
            live_matches_data["Third Match"] = "Match not found"
            self.logger.error(F"LIVE_MATCHES_ERROR: {error}")

        return live_matches_data

    def parse_top_organization(self, response: Response, **kwargs) -> dict:

        top_container = response.xpath(
            "//*[@id='top_blocks']//*[contains(@class, 'col-span-12')]"
        )

        team_names_by_tournaments_count = top_container[0].xpath(
            ".//*[contains(@class, 'logo')]/@title"
        ).getall()
        teams_tournaments_count = top_container[0].xpath(
            './/div[@class="value text-center !text-xs"]/@data-tippy-content'
        ).getall()
        team_tournament_dict = dict(
            zip(team_names_by_tournaments_count, teams_tournaments_count))

        team_names_by_matches_count = top_container[1].xpath(
            ".//*[contains(@class, 'logo')]/@title").getall()
        teams_matches_count = top_container[1].xpath(
            './/div[@class="value text-center !text-xs"]/@data-tippy-content').getall()
        team_matches_dict = dict(
            zip(team_names_by_matches_count, teams_matches_count))

        games = top_container[2].xpath(
            ".//*[contains(@class, 'logo')]/@title").getall()
        teams_by_viewers_count = top_container[2].xpath(
            './/div[@class="value text-center !text-xs"]/@data-tippy-content').getall()
        team_viewers_dict = dict(zip(games, teams_by_viewers_count))

        top_organization = {
            "Top Organization by Tournaments Count": team_tournament_dict,
            "Top Organization by Matches Count": team_matches_dict,
            "Top Games by Viewers Count": team_viewers_dict,
        }

        return top_organization
