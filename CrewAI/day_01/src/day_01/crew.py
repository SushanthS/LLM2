from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from day_01.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class Day01Crew:
	"""Day01 crew"""

	@agent
	def joke_creator(self) -> Agent:
		return Agent(
			config=self.agents_config['joke_creator'],
			verbose=True
		)

	@agent
	def add_emojis(self) -> Agent:
		return Agent(
			config=self.agents_config['add_emojis'],
			verbose=True
		)

	@task
	def joke_task(self) -> Task:
		return Task(
			config=self.tasks_config['joke_task'],
		)

	@task
	def add_emojis_task(self) -> Task:
		return Task(
			config=self.tasks_config['add_emojis_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Day01 crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)