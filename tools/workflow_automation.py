"""
AI-powered workflow automation and task orchestration.

Helps create, manage, and optimize workflows using AI assistance.
"""

from typing import Dict, Any, Optional, List
from openai import OpenAI
import os
from datetime import datetime


class WorkflowAutomation:
    """
    AI-powered workflow automation assistant.
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the workflow automation tool.
        
        Args:
            model_name: OpenAI model to use
        """
        self.model_name = model_name
        self.client = None
        
        # Initialize OpenAI client if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
    
    def suggest_workflow(
        self,
        task_description: str,
        constraints: Optional[List[str]] = None,
        tools_available: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Suggest an optimal workflow for a given task.
        
        Args:
            task_description: Description of the task or goal
            constraints: List of constraints (e.g., time, resources)
            tools_available: List of available tools or platforms
        
        Returns:
            Dictionary containing suggested workflow
        """
        if not task_description or not task_description.strip():
            return {
                "workflow": None,
                "status": "error",
                "error": "Task description cannot be empty"
            }
        
        if not self.client:
            return {
                "workflow": None,
                "status": "not_configured",
                "error": "OpenAI API key not configured"
            }
        
        try:
            prompt_parts = [
                f"Suggest an optimal workflow for the following task: {task_description}",
                "\nProvide the workflow as a numbered list of steps with descriptions."
            ]
            
            if constraints:
                prompt_parts.append(f"\nConstraints:\n" + "\n".join(f"- {c}" for c in constraints))
            
            if tools_available:
                prompt_parts.append(f"\nAvailable tools:\n" + "\n".join(f"- {t}" for t in tools_available))
            
            prompt = "\n".join(prompt_parts)
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at workflow optimization and task automation. Provide clear, actionable workflows."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.5
            )
            
            workflow_text = response.choices[0].message.content.strip()
            
            # Parse steps
            steps = self._parse_workflow_steps(workflow_text)
            
            return {
                "workflow": workflow_text,
                "steps": steps,
                "status": "success",
                "model": self.model_name,
                "generated_at": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            return {
                "workflow": None,
                "status": "error",
                "error": str(e)
            }
    
    def _parse_workflow_steps(self, workflow_text: str) -> List[Dict[str, Any]]:
        """Parse workflow text into structured steps."""
        steps = []
        lines = workflow_text.split('\n')
        
        current_step = None
        for line in lines:
            line = line.strip()
            # Look for numbered steps
            if line and (line[0].isdigit() or line.startswith('-')):
                # Extract step number and description
                parts = line.split('.', 1) if '.' in line else line.split(' ', 1)
                if len(parts) >= 2:
                    step_num = parts[0].strip('.-').strip()
                    description = parts[1].strip()
                    current_step = {
                        "step": step_num,
                        "description": description
                    }
                    steps.append(current_step)
        
        return steps
    
    def optimize_workflow(
        self,
        current_workflow: str,
        optimization_goals: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Optimize an existing workflow.
        
        Args:
            current_workflow: Current workflow description
            optimization_goals: Goals for optimization (e.g., "reduce time", "automate more steps")
        
        Returns:
            Dictionary containing optimized workflow
        """
        if not current_workflow or not current_workflow.strip():
            return {
                "optimized_workflow": None,
                "status": "error",
                "error": "Current workflow cannot be empty"
            }
        
        if not self.client:
            return {
                "optimized_workflow": None,
                "status": "not_configured",
                "error": "OpenAI API key not configured"
            }
        
        try:
            prompt = f"Optimize the following workflow:\n\n{current_workflow}\n\n"
            
            if optimization_goals:
                prompt += "Optimization goals:\n" + "\n".join(f"- {goal}" for goal in optimization_goals)
            else:
                prompt += "Goals: Reduce time, increase efficiency, and automate where possible."
            
            prompt += "\n\nProvide the optimized workflow with explanations of changes made."
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at workflow optimization and process improvement."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.5
            )
            
            optimized_workflow = response.choices[0].message.content.strip()
            
            return {
                "optimized_workflow": optimized_workflow,
                "original_workflow": current_workflow,
                "status": "success",
                "model": self.model_name
            }
        
        except Exception as e:
            return {
                "optimized_workflow": None,
                "status": "error",
                "error": str(e)
            }
    
    def identify_bottlenecks(
        self,
        workflow: str
    ) -> Dict[str, Any]:
        """
        Identify potential bottlenecks in a workflow.
        
        Args:
            workflow: Workflow description
        
        Returns:
            Dictionary containing identified bottlenecks and suggestions
        """
        if not workflow or not workflow.strip():
            return {
                "bottlenecks": [],
                "status": "error",
                "error": "Workflow cannot be empty"
            }
        
        if not self.client:
            return {
                "bottlenecks": [],
                "status": "not_configured",
                "error": "OpenAI API key not configured"
            }
        
        try:
            prompt = f"""Analyze the following workflow and identify potential bottlenecks:

{workflow}

For each bottleneck, provide:
1. The step or area affected
2. Why it's a bottleneck
3. Suggested solution

Format as a numbered list."""
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at identifying process bottlenecks and inefficiencies."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.4
            )
            
            analysis = response.choices[0].message.content.strip()
            
            return {
                "analysis": analysis,
                "status": "success",
                "model": self.model_name
            }
        
        except Exception as e:
            return {
                "bottlenecks": [],
                "status": "error",
                "error": str(e)
            }
    
    def generate_automation_script(
        self,
        workflow: str,
        target_platform: str = "python"
    ) -> Dict[str, Any]:
        """
        Generate automation script code for a workflow.
        
        Args:
            workflow: Workflow description
            target_platform: Target platform/language (python, javascript, bash)
        
        Returns:
            Dictionary containing automation script
        """
        if not workflow or not workflow.strip():
            return {
                "script": None,
                "status": "error",
                "error": "Workflow cannot be empty"
            }
        
        if not self.client:
            return {
                "script": None,
                "status": "not_configured",
                "error": "OpenAI API key not configured"
            }
        
        try:
            prompt = f"""Generate a {target_platform} automation script for the following workflow:

{workflow}

Provide well-commented, production-ready code that implements this workflow.
Include error handling and logging."""
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert {target_platform} developer who creates robust automation scripts."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            script = response.choices[0].message.content.strip()
            
            return {
                "script": script,
                "platform": target_platform,
                "status": "success",
                "model": self.model_name
            }
        
        except Exception as e:
            return {
                "script": None,
                "status": "error",
                "error": str(e)
            }


# Example usage instance
workflow_automation = WorkflowAutomation()
