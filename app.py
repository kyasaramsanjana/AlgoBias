from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        file = request.files['file']
        df = pd.read_csv(file)
        
        results = {}
        bias_report = []
        sensitive_cols = []
        
        for col in df.columns:
            if any(word in col.lower() for word in ['gender', 'race', 'age', 'religion', 'sex', 'ethnicity']):
                sensitive_cols.append(col)
        
        for col in sensitive_cols:
            value_counts = df[col].value_counts(normalize=True) * 100
            bias_report.append({
                'column': col,
                'distribution': value_counts.to_dict()
            })
        
        results['sensitive_columns'] = sensitive_cols
        results['bias_report'] = bias_report
        results['total_rows'] = int(len(df))
        results['total_columns'] = int(len(df.columns))
        results['columns'] = list(df.columns)
        
        return jsonify({'success': True, 'results': results})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)