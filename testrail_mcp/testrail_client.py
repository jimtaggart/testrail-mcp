"""TestRail API client module."""
import base64
import json
from typing import Dict, List, Any, Optional, Union
import requests
from urllib.parse import urlencode

class TestRailClient:
    """TestRail API client for interacting with TestRail."""

    def __init__(self, base_url: str, username: str, api_key: str):
        """
        Initialize the TestRail API client.
        
        Args:
            base_url: The URL of your TestRail instance (e.g., [https://example.testrail.io/)](https://example.testrail.io/))
            username: Your TestRail username/email
            api_key: Your TestRail API key
        """
        self.username = username
        self.api_key = api_key
        
        # Ensure the base URL ends with a slash
        if not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url + 'index.php?/api/v2/'
        
        # Set up the session with authentication
        self.session = requests.Session()
        auth = str(
            base64.b64encode(
                bytes(f'{username}:{api_key}', 'utf-8')
            ),
            'ascii'
        ).strip()
        self.session.headers.update({
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json',
        })

    def _send_request(self, method: str, uri: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Any:
        """
        Send a request to the TestRail API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            uri: API endpoint URI
            data: Request data for POST/PUT requests
            params: Query parameters for GET requests
            
        Returns:
            Response data from TestRail
            
        Raises:
            Exception: If the request fails
        """
        url = self.base_url + uri
        
        # Add query parameters for GET requests
        if params and method.upper() == 'GET':
            # Filter out None values
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = urlencode(filtered_params)
                # Use & if URL already has query parameters, otherwise use ?
                separator = '&' if '?' in url else '?'
                url += separator + query_string
        
        if method.upper() == 'GET':
            response = self.session.get(url)
        elif method.upper() == 'POST':
            response = self.session.post(url, data=json.dumps(data) if data else None)
        elif method.upper() == 'PUT':
            response = self.session.put(url, data=json.dumps(data) if data else None)
        elif method.upper() == 'DELETE':
            response = self.session.delete(url)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
            
        if response.status_code >= 300:
            try:
                error = response.json()
            except:
                error = response.text
            debug_info = f" [URL: {url}]"
            if params:
                debug_info += f" [Original params: {params}]"
            raise Exception(f"TestRail API returned HTTP {response.status_code}: {error}{debug_info}")
            
        return response.json() if response.content else {}

    # Cases API
    def get_case(self, case_id: int) -> Dict:
        """Get a test case by ID."""
        return self._send_request('GET', f'get_case/{case_id}')
    
    def get_cases(self, project_id: int, suite_id: Optional[int] = None) -> List[Dict]:
        """Get all test cases for a project/suite."""
        params = {}
        if suite_id is not None:
            params['suite_id'] = suite_id
        return self._send_request('GET', f'get_cases/{project_id}', params=params)
    
    def add_case(self, section_id: int, data: Dict) -> Dict:
        """Add a new test case."""
        return self._send_request('POST', f'add_case/{section_id}', data)
    
    def update_case(self, case_id: int, data: Dict) -> Dict:
        """Update an existing test case."""
        return self._send_request('POST', f'update_case/{case_id}', data)
    
    def delete_case(self, case_id: int) -> Dict:
        """Delete a test case."""
        return self._send_request('POST', f'delete_case/{case_id}')

    # Projects API
    def get_project(self, project_id: int) -> Dict:
        """Get a project by ID."""
        return self._send_request('GET', f'get_project/{project_id}')
    
    def get_projects(self) -> List[Dict]:
        """Get all projects."""
        return self._send_request('GET', 'get_projects')
    
    def add_project(self, data: Dict) -> Dict:
        """Add a new project."""
        return self._send_request('POST', 'add_project', data)
    
    def update_project(self, project_id: int, data: Dict) -> Dict:
        """Update an existing project."""
        return self._send_request('POST', f'update_project/{project_id}', data)
    
    def delete_project(self, project_id: int) -> Dict:
        """Delete a project."""
        return self._send_request('POST', f'delete_project/{project_id}')

    # Runs API
    def get_run(self, run_id: int) -> Dict:
        """Get a test run by ID."""
        return self._send_request('GET', f'get_run/{run_id}')
    
    def get_runs(self, project_id: int) -> List[Dict]:
        """Get all test runs for a project."""
        return self._send_request('GET', f'get_runs/{project_id}')
    
    def add_run(self, project_id: int, data: Dict) -> Dict:
        """Add a new test run."""
        return self._send_request('POST', f'add_run/{project_id}', data)
    
    def update_run(self, run_id: int, data: Dict) -> Dict:
        """Update an existing test run."""
        return self._send_request('POST', f'update_run/{run_id}', data)
    
    def close_run(self, run_id: int) -> Dict:
        """Close a test run."""
        return self._send_request('POST', f'close_run/{run_id}')
    
    def delete_run(self, run_id: int) -> Dict:
        """Delete a test run."""
        return self._send_request('POST', f'delete_run/{run_id}')

    # Results API
    def get_results(self, test_id: int) -> List[Dict]:
        """Get all test results for a test."""
        return self._send_request('GET', f'get_results/{test_id}')
    
    def add_result(self, test_id: int, data: Dict) -> Dict:
        """Add a new test result."""
        return self._send_request('POST', f'add_result/{test_id}', data)

    # Datasets API
    def get_dataset(self, dataset_id: int) -> Dict:
        """Get a dataset by ID."""
        return self._send_request('GET', f'get_dataset/{dataset_id}')
    
    def get_datasets(self, project_id: int) -> List[Dict]:
        """Get all datasets for a project."""
        return self._send_request('GET', f'get_datasets/{project_id}')
    
    def add_dataset(self, project_id: int, data: Dict) -> Dict:
        """Add a new dataset."""
        return self._send_request('POST', f'add_dataset/{project_id}', data)
    
    def update_dataset(self, dataset_id: int, data: Dict) -> Dict:
        """Update an existing dataset."""
        return self._send_request('POST', f'update_dataset/{dataset_id}', data)
    
    def delete_dataset(self, dataset_id: int) -> Dict:
        """Delete a dataset."""
        return self._send_request('POST', f'delete_dataset/{dataset_id}')

    # Suites API
    def get_suite(self, suite_id: int) -> Dict:
        """Get a suite by ID."""
        return self._send_request('GET', f'get_suite/{suite_id}')
    
    def get_suites(self, project_id: int) -> List[Dict]:
        """Get all suites for a project."""
        return self._send_request('GET', f'get_suites/{project_id}')

    # Sections API
    def get_section(self, section_id: int) -> Dict:
        """Get a specific section"""
        return self._send_request('GET', f'get_section/{section_id}')

    def get_sections(self, project_id: int, suite_id: Optional[int] = None, params: Optional[Dict] = None) -> Dict:
        """Get all sections for a project"""
        query_params = params or {}
        if suite_id is not None:
            query_params['suite_id'] = suite_id
        return self._send_request('GET', f'get_sections/{project_id}', params=query_params)

    def add_section(self, project_id: int, data: Dict) -> Dict:
        """Add a new section"""
        return self._send_request('POST', f'add_section/{project_id}', data)

    def update_section(self, section_id: int, data: Dict) -> Dict:
        """Update an existing section"""
        return self._send_request('POST', f'update_section/{section_id}', data)

    def delete_section(self, section_id: int, soft: bool) -> Dict:
        """Delete an existing section"""
        url = f'delete_section/{section_id}'
        if soft:
            url = f'delete_section/{section_id}?soft=1'
        return self._send_request('POST', url)

    def move_section(self, section_id: int, data: Dict) -> Dict:
        """Move a section to a different parent or position"""
        return self._send_request('POST', f'move_section/{section_id}', data)