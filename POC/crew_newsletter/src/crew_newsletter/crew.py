from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import Any, Optional, Type

from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool
)

from tools.custom_tool import RedditTool, YoutubeTool

@CrewBase
class NewsletterCrew():
	"""Newsletter crew"""

	reddit_topic: Optional[str] = "latest ai development"
	youtube_topic: Optional[str] = "#ai #llms"
	max_results: Optional[int] = 10
	reddit_tool: Type[RedditTool] = None
	youtube_tool: Type[YoutubeTool] = None

	def __init__(self, *args, **kwargs):
		super().__init__()
		self.reddit_topic = kwargs.get("reddit_topic", self.reddit_topic)
		self.youtube_topic = kwargs.get("youtube_topic", self.youtube_topic)
		self.max_results = kwargs.get("max_results", self.max_results)
		self.reddit_tool = RedditTool(reddit_topic=self.reddit_topic, max_results=self.max_results)
		self.youtube_tool = YoutubeTool(hashtags=self.youtube_topic, max_results=self.max_results)

	@agent
	def subject_matter_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['subject_matter_expert'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			tools=[self.reddit_tool, self.youtube_tool]
		)

	# @agent
	# def reviewer(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['reviewer'],
	# 		# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
	# 		verbose=True
	# 	)
	
	# @agent
	# def writer(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['writer'],
	# 		# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
	# 		verbose=True
	# 	)
	
	# @agent
	# def editor(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['editor'],
	# 		# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
	# 		verbose=True
	# 	)
	
	# @agent
	# def coder(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['coder'],
	# 		# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
	# 		verbose=True
	# 	)

	# @agent
	# def code_reviewer(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['senior_code_reviewer'],
	# 		# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
	# 		verbose=True
	# 	)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			output_file='research.md'
		)

	# @task
	# def reviewing_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['reviewing_task'],
	# 		# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
	# 		output_file='research_reviewed.md'
	# 	)
	
	# @task
	# def writing_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['writing_task'],
	# 		# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
	# 		output_file='summaries.md'
	# 	)
	
	# @task
	# def editing_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['editing_task'],
	# 		# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
	# 		output_file='editorial.md'
	# 	)
	
	# @task
	# def review_editing_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['review_editing_task'],
	# 		# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
	# 		output_file='reviewed_editorial.md'
	# 	)
	
	# @task
	# def coding_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['coding_task'],
	# 		# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
	# 		output_file='raw_newsletter.py'
	# 	)

	# @task
	# def review_coding_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['review_coding_task'],
	# 		# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
	# 		output_file='newsletter.py'
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the Newsletter crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)