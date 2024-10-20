from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from newsletter.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class NewsletterCrew():
	"""Newsletter crew"""

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def expert(self) -> Agent:
		return Agent(
			config=self.agents_config['expert'],
			verbose=True
		)
	
	@agent
	def expert(self) -> Agent:
		return Agent(
			config=self.agents_config['planner'],
			verbose=True
		)
	
	@agent
	def expert(self) -> Agent:
		return Agent(
			config=self.agents_config['reviewer'],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def fact_check_task(self) -> Task:
		return Task(
			config=self.tasks_config['expert'],
			output_file='fact_check.md'
		)

	@task
	def article_planning_task(self) -> Task:
		return Task(
			config=self.tasks_config['planner'],
			output_file='article_planning.md'
		)
	
	@task
	def article_review_task(self) -> Task:
		return Task(
			config=self.tasks_config['reviewer'],
			output_file='article_review.md'
		)

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