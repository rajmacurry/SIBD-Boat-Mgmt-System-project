#!d:/Study materials/Portugal/P2/SIBD/Project/second part/venv/Scripts/python.exe

def print_header(title="Sailing Project"):
    print("Content-type:text/html\n\n")
    print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>""" + title + """</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {
            /* Nautical Theme Background */
            background-image: url('https://images.unsplash.com/photo-1549646429-cda9f928a3bd?q=80&w=2070&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-color: #0f172a; /* Fallback dark blue */
            font-family: 'Open Sans', sans-serif;
            min-height: 100vh;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            color: #0c344e; /* Dark Navy */
        }

        /* Glassmorphism Container */
        .glass-panel {
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 2.5rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
            margin-top: 3rem;
            margin-bottom: 3rem;
            border: 1px solid rgba(255, 255, 255, 0.4);
        }

        /* Buttons */
        .btn-primary {
            background-color: #0ea5e9; /* Ocean Blue */
            border-color: #0ea5e9;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 10px 24px;
            transition: all 0.3s ease;
        }
        
        .btn-primary:hover {
            background-color: #0284c7;
            border-color: #0284c7;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
        }

        .btn-secondary {
            background-color: #64748b;
            border-color: #64748b;
        }

        /* Forms */
        .form-label {
            font-weight: 600;
            color: #334155;
        }
        
        .form-control, .form-select {
            border-radius: 8px;
            padding: 12px;
            border: 2px solid #e2e8f0;
        }
        
        .form-control:focus, .form-select:focus {
            border-color: #0ea5e9;
            box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.1);
        }

        /* Menu Links */
        .menu-link {
            display: block;
            padding: 1.5rem;
            background: rgba(241, 245, 249, 0.8);
            border-radius: 12px;
            text-decoration: none;
            color: #334155;
            font-weight: 700;
            font-size: 1.2rem;
            transition: all 0.3s ease;
            text-align: center;
            border: 2px solid transparent;
        }

        .menu-link:hover {
            background: #fff;
            color: #0ea5e9;
            transform: scale(1.02);
            border-color: #0ea5e9;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        
        .card {
            border: none;
            background: transparent;
        }

        /* Tables */
        .table thead th {
            background-color: #0f172a;
            color: white;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85rem;
            border: none;
        }
        
        .table-striped > tbody > tr:nth-of-type(odd) > * {
            background-color: rgba(14, 165, 233, 0.05);
        }
        
        .table-hover > tbody > tr:hover > * {
            background-color: rgba(14, 165, 233, 0.15);
        }
        
        td {
            vertical-align: middle;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="main-content">
            <div class="glass-panel">
""")

def print_footer():
    print("""
            </div> <!-- End glass-panel -->
        </div>
    </div>
    
    <!-- Bootstrap 5 JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")
