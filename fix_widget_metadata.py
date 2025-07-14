#!/usr/bin/env python3
"""
Fix notebook widget metadata structure for nbconvert compatibility.

This script restructures the widget metadata to include the required 'state' key
at the top level of the widget-state+json section.
"""

import nbformat

def fix_widget_metadata(notebook_path):
    """
    Fix the widget metadata structure to be compatible with nbconvert.
    
    Args:
        notebook_path: Path to the notebook file to fix
    """
    print(f"Loading notebook: {notebook_path}")
    
    # Load the notebook
    nb = nbformat.read(notebook_path, as_version=4)
    
    # Get the widget metadata
    widgets = nb.metadata.get('widgets', {})
    widget_state_key = 'application/vnd.jupyter.widget-state+json'
    
    if widget_state_key not in widgets:
        print("No widget state found in notebook metadata")
        return
    
    widget_state = widgets[widget_state_key]
    
    # Check if 'state' key already exists at the top level
    if 'state' in widget_state:
        print("✓ Widget metadata already has 'state' key at top level")
        return
    
    print("✗ Widget metadata missing 'state' key at top level")
    print(f"Found {len(widget_state)} widget definitions")
    
    # Restructure the widget metadata
    # The correct structure should be:
    # {
    #   "application/vnd.jupyter.widget-state+json": {
    #     "state": {
    #       "widget_id": {
    #         "model_module": "...",
    #         "model_name": "...",
    #         "state": { ... }
    #       }
    #     }
    #   }
    # }
    
    # Create the new structure
    new_widget_state = {
        "state": widget_state
    }
    
    # Update the notebook metadata
    nb.metadata['widgets'][widget_state_key] = new_widget_state
    
    print("✓ Added 'state' key at top level")
    
    # Save the fixed notebook
    backup_path = notebook_path + '.backup'
    print(f"Creating backup: {backup_path}")
    
    # Create backup
    with open(backup_path, 'w') as f:
        nbformat.write(nb, f)
    
    # Save the fixed notebook
    print(f"Saving fixed notebook: {notebook_path}")
    nbformat.write(nb, notebook_path)
    
    print("✅ Notebook widget metadata fixed successfully!")

if __name__ == "__main__":
    # Fix both notebooks
    notebooks = ["Model_Pruning.ipynb", "C4AIScholarsChallenge_2022.ipynb"]
    
    for notebook in notebooks:
        print(f"\n{'='*50}")
        print(f"Processing: {notebook}")
        print(f"{'='*50}")
        try:
            fix_widget_metadata(notebook)
        except Exception as e:
            print(f"❌ Error processing {notebook}: {e}")
        
    print(f"\n{'='*50}")
    print("✅ All notebooks processed!")
    print(f"{'='*50}")
