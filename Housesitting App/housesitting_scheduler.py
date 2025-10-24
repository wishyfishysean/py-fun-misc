"""
Housesitting Scheduler App
A fully functional offline scheduling application for managing housesitting bookings.

Requirements:
- Python 3.7+
- pip install webview

To run:
    python housesitting_scheduler.py

To create executable:
    pip install pyinstaller
    pyinstaller --onefile --windowed --name "HousesitScheduler" housesitting_scheduler.py

Author: Claude & Me
Version: 2.0
"""

import webview
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import csv
from typing import Dict, List, Optional

class BookingManager:
    """Manages all booking data and operations"""
    
    def __init__(self, data_file: str = "bookings.json"):
        """Initialize the booking manager with a data file"""
        self.data_file = self._get_data_path(data_file)
        self.bookings = self._load_bookings()
    
    def _get_data_path(self, filename: str) -> str:
        """Get the correct path for the data file (works with PyInstaller)"""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            app_dir = os.path.dirname(sys.executable)
        else:
            # Running as script
            app_dir = os.path.dirname(os.path.abspath(__file__))
        
        return os.path.join(app_dir, filename)
    
    def _load_bookings(self) -> Dict:
        """Load bookings from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading bookings: {e}")
                return {}
        return {}
    
    def _save_bookings(self) -> bool:
        """Save bookings to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.bookings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving bookings: {e}")
            return False
    
    def add_booking(self, date: str, client: str, notes: str, price: str = "") -> Dict:
        """Add a new booking"""
        booking_id = f"booking_{datetime.now().timestamp()}"
        self.bookings[date] = {
            'id': booking_id,
            'date': date,
            'client': client,
            'notes': notes,
            'price': price,
            'created': datetime.now().isoformat()
        }
        self._save_bookings()
        return self.bookings[date]
    
    def update_booking(self, date: str, client: str, notes: str, price: str = "") -> Optional[Dict]:
        """Update an existing booking"""
        if date in self.bookings:
            self.bookings[date]['client'] = client
            self.bookings[date]['notes'] = notes
            self.bookings[date]['price'] = price
            self.bookings[date]['modified'] = datetime.now().isoformat()
            self._save_bookings()
            return self.bookings[date]
        return None
    
    def delete_booking(self, date: str) -> bool:
        """Delete a booking"""
        if date in self.bookings:
            del self.bookings[date]
            self._save_bookings()
            return True
        return False
    
    def get_booking(self, date: str) -> Optional[Dict]:
        """Get a specific booking"""
        return self.bookings.get(date)
    
    def get_all_bookings(self) -> Dict:
        """Get all bookings"""
        return self.bookings
    
    def search_bookings(self, query: str) -> Dict:
        """Search bookings by client name or notes"""
        query_lower = query.lower()
        results = {}
        for date, booking in self.bookings.items():
            if (query_lower in booking['client'].lower() or 
                query_lower in booking['notes'].lower()):
                results[date] = booking
        return results
    
    def export_to_csv(self, filepath: str) -> bool:
        """Export all bookings to CSV"""
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Client', 'Price', 'Notes', 'Created'])
                
                for date in sorted(self.bookings.keys()):
                    booking = self.bookings[date]
                    writer.writerow([
                        booking['date'],
                        booking['client'],
                        booking.get('price', ''),
                        booking['notes'],
                        booking.get('created', '')
                    ])
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False


class API:
    """API class to handle communication between Python backend and JS frontend"""
    
    def __init__(self):
        """Initialize the API with a booking manager"""
        self.manager = BookingManager()
    
    def get_bookings(self) -> str:
        """Get all bookings as JSON string"""
        return json.dumps(self.manager.get_all_bookings())
    
    def add_booking(self, date: str, client: str, notes: str, price: str = "") -> str:
        """Add a new booking"""
        result = self.manager.add_booking(date, client, notes, price)
        return json.dumps({'success': True, 'booking': result})
    
    def update_booking(self, date: str, client: str, notes: str, price: str = "") -> str:
        """Update an existing booking"""
        result = self.manager.update_booking(date, client, notes, price)
        if result:
            return json.dumps({'success': True, 'booking': result})
        return json.dumps({'success': False, 'error': 'Booking not found'})
    
    def delete_booking(self, date: str) -> str:
        """Delete a booking"""
        success = self.manager.delete_booking(date)
        return json.dumps({'success': success})
    
    def get_booking(self, date: str) -> str:
        """Get a specific booking"""
        booking = self.manager.get_booking(date)
        if booking:
            return json.dumps({'success': True, 'booking': booking})
        return json.dumps({'success': False, 'error': 'Booking not found'})
    
    def search_bookings(self, query: str) -> str:
        """Search bookings"""
        results = self.manager.search_bookings(query)
        return json.dumps(results)
    
    def export_csv(self) -> str:
        """Export bookings to CSV"""
        filepath = self.manager._get_data_path('housesitting_bookings.csv')
        success = self.manager.export_to_csv(filepath)
        return json.dumps({
            'success': success,
            'filepath': filepath if success else None
        })


# HTML/CSS/JS Frontend
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Housesitting Scheduler</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary-color: #667eea;
            --primary-hover: #5568d3;
            --secondary-color: #764ba2;
            --bg-gradient-start: #667eea;
            --bg-gradient-end: #764ba2;
            --text-color: #333;
            --bg-color: #ffffff;
            --bg-secondary: #f8f9fa;
            --border-color: #e9ecef;
            --card-bg: #ffffff;
            --shadow: rgba(0,0,0,0.1);
            --shadow-hover: rgba(0,0,0,0.15);
        }
        
        body.dark-mode {
            --primary-color: #7c93ee;
            --primary-hover: #8da4f0;
            --bg-gradient-start: #4a5f9f;
            --bg-gradient-end: #5a3d7a;
            --text-color: #e0e0e0;
            --bg-color: #1a1a1a;
            --bg-secondary: #2a2a2a;
            --border-color: #3a3a3a;
            --card-bg: #252525;
            --shadow: rgba(0,0,0,0.3);
            --shadow-hover: rgba(0,0,0,0.5);
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
            min-height: 100vh;
            color: var(--text-color);
            transition: all 0.3s ease;
        }
        
        .app-container {
            display: flex;
            height: 100vh;
        }
        
        /* Sidebar */
        .sidebar {
            width: 320px;
            background: var(--card-bg);
            border-right: 2px solid var(--border-color);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 2px 0 10px var(--shadow);
        }
        
        .sidebar-header {
            padding: 25px;
            background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
            color: white;
        }
        
        .sidebar-header h2 {
            font-size: 1.3em;
            margin-bottom: 5px;
        }
        
        .sidebar-header p {
            font-size: 0.9em;
            opacity: 0.9;
        }
        
        .bookings-list {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
        }
        
        .booking-item {
            background: var(--bg-secondary);
            border: 2px solid var(--border-color);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .booking-item:hover {
            border-color: var(--primary-color);
            transform: translateX(5px);
            box-shadow: 0 3px 10px var(--shadow-hover);
        }
        
        .booking-date {
            font-weight: 700;
            font-size: 1.1em;
            color: var(--primary-color);
            margin-bottom: 5px;
        }
        
        .booking-client {
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .booking-summary {
            font-size: 0.9em;
            color: var(--text-color);
            opacity: 0.8;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .booking-price {
            font-size: 0.9em;
            color: var(--primary-color);
            font-weight: 600;
            margin-top: 5px;
        }
        
        .no-bookings {
            text-align: center;
            padding: 30px;
            color: var(--text-color);
            opacity: 0.6;
        }
        
        /* Main Content */
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .container {
            flex: 1;
            display: flex;
            flex-direction: column;
            margin: 20px;
            background: var(--card-bg);
            border-radius: 15px;
            box-shadow: 0 20px 60px var(--shadow);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .controls {
            padding: 20px 30px;
            background: var(--bg-secondary);
            border-bottom: 2px solid var(--border-color);
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }
        
        .search-box {
            flex: 1;
            min-width: 200px;
        }
        
        .search-box input {
            width: 100%;
            padding: 12px 20px;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            font-size: 1em;
            transition: all 0.3s;
            background: var(--card-bg);
            color: var(--text-color);
        }
        
        .search-box input:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .theme-controls {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        
        .color-picker-btn {
            width: 40px;
            height: 40px;
            border-radius: 8px;
            border: 2px solid var(--border-color);
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .color-picker-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 3px 10px var(--shadow-hover);
        }
        
        .toggle-switch {
            position: relative;
            display: inline-block;
            width: 50px;
            height: 26px;
        }
        
        .toggle-switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 26px;
        }
        
        .slider:before {
            position: absolute;
            content: "";
            height: 18px;
            width: 18px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }
        
        input:checked + .slider {
            background-color: var(--primary-color);
        }
        
        input:checked + .slider:before {
            transform: translateX(24px);
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 600;
        }
        
        .btn-primary {
            background: var(--primary-color);
            color: white;
        }
        
        .btn-primary:hover {
            background: var(--primary-hover);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px var(--shadow-hover);
        }
        
        .btn-large {
            padding: 15px 30px;
            font-size: 1.2em;
        }
        
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #5a6268;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px var(--shadow-hover);
        }
        
        .btn-danger {
            background: #dc3545;
            color: white;
        }
        
        .btn-danger:hover {
            background: #c82333;
        }
        
        .quick-add-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--primary-color);
            color: white;
            font-size: 2em;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 5px 20px var(--shadow-hover);
            z-index: 100;
            border: none;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .quick-add-btn:hover {
            transform: scale(1.1) rotate(90deg);
        }
        
        .calendar-nav {
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--card-bg);
        }
        
        .calendar-nav h2 {
            font-size: 1.8em;
            color: var(--text-color);
        }
        
        .nav-buttons {
            display: flex;
            gap: 10px;
        }
        
        .nav-btn {
            padding: 8px 16px;
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
        }
        
        .nav-btn:hover {
            background: var(--primary-hover);
        }
        
        .calendar {
            padding: 30px;
            flex: 1;
            overflow-y: auto;
        }
        
        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 10px;
        }
        
        .day-header {
            text-align: center;
            font-weight: 600;
            padding: 15px;
            background: var(--bg-secondary);
            border-radius: 8px;
            color: var(--text-color);
        }
        
        .day {
            aspect-ratio: 1;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            padding: 10px;
            cursor: pointer;
            transition: all 0.3s;
            background: var(--card-bg);
            display: flex;
            flex-direction: column;
            position: relative;
        }
        
        .day:hover {
            border-color: var(--primary-color);
            transform: scale(1.05);
            box-shadow: 0 5px 15px var(--shadow-hover);
        }
        
        .day.other-month {
            opacity: 0.3;
        }
        
        .day.today {
            border-color: #28a745;
            background: #d4edda;
        }
        
        body.dark-mode .day.today {
            background: #1e4d2b;
            border-color: #5cb85c;
        }
        
        .day.booked {
            background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
            color: white;
            border-color: var(--primary-color);
        }
        
        .day-number {
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .day-client {
            font-size: 0.85em;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        
        .modal.active {
            display: flex;
        }
        
        .modal-content {
            background: var(--card-bg);
            border-radius: 15px;
            width: 90%;
            max-width: 600px;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 20px 60px var(--shadow);
        }
        
        .modal-header {
            background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
            color: white;
            padding: 25px;
            border-radius: 15px 15px 0 0;
        }
        
        .modal-header h2 {
            font-size: 1.8em;
        }
        
        .modal-body {
            padding: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: var(--text-color);
        }
        
        .form-group input,
        .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            font-size: 1em;
            font-family: inherit;
            transition: all 0.3s;
            background: var(--card-bg);
            color: var(--text-color);
        }
        
        .form-group textarea {
            min-height: 120px;
            resize: vertical;
        }
        
        .form-group input:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .modal-footer {
            padding: 20px 30px;
            background: var(--bg-secondary);
            display: flex;
            gap: 10px;
            justify-content: flex-end;
            border-radius: 0 0 15px 15px;
        }
        
        .alert {
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        
        .alert.show {
            display: block;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .stats {
            padding: 20px 30px;
            background: var(--bg-secondary);
            display: flex;
            gap: 20px;
            justify-content: space-around;
            flex-wrap: wrap;
        }
        
        .stat-card {
            background: var(--card-bg);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            min-width: 150px;
            box-shadow: 0 2px 8px var(--shadow);
        }
        
        .stat-card .number {
            font-size: 2.5em;
            font-weight: 700;
            color: var(--primary-color);
        }
        
        .stat-card .label {
            color: var(--text-color);
            opacity: 0.7;
            margin-top: 5px;
        }
        
        @media (max-width: 768px) {
            .sidebar {
                width: 100%;
                max-height: 40vh;
            }
            
            .app-container {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Sidebar with bookings list -->
        <div class="sidebar">
            <div class="sidebar-header">
                <h2>Upcoming Bookings</h2>
                <p id="bookingCount">0 bookings scheduled</p>
            </div>
            <div class="bookings-list" id="bookingsList">
                <div class="no-bookings">No bookings yet. Click a day on the calendar or use the + button to add one.</div>
            </div>
        </div>
        
        <!-- Main content area -->
        <div class="main-content">
            <div class="container">
                <div class="header">
                    <h1>Housesitting Scheduler</h1>
                    <p>Manage Housesitting Bookings & Duties</p>
                </div>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="number" id="totalBookings">0</div>
                        <div class="label">Total Bookings</div>
                    </div>
                    <div class="stat-card">
                        <div class="number" id="thisMonthBookings">0</div>
                        <div class="label">This Month</div>
                    </div>
                </div>
                
                <div class="controls">
                    <div class="search-box">
                        <input type="text" id="searchInput" placeholder="Search bookings by client or notes...">
                    </div>
                    
                    <div class="theme-controls">
                        <input type="color" id="colorPicker" class="color-picker-btn" title="Change theme color">
                        
                        <label class="toggle-switch" title="Dark mode">
                            <input type="checkbox" id="darkModeToggle">
                            <span class="slider"></span>
                        </label>
                    </div>
                    
                    <button class="btn btn-primary" onclick="app.exportCSV()">Export CSV</button>
                    <button class="btn btn-secondary" onclick="app.showToday()">Today</button>
                </div>
                
                <div class="calendar-nav">
                    <div class="nav-buttons">
                        <button class="nav-btn" onclick="app.prevMonth()">Previous</button>
                    </div>
                    <h2 id="currentMonth">Loading...</h2>
                    <div class="nav-buttons">
                        <button class="nav-btn" onclick="app.nextMonth()">Next</button>
                    </div>
                </div>
                
                <div class="calendar">
                    <div class="calendar-grid" id="calendar">
                        <!-- Calendar will be generated here -->
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Quick add button -->
    <button class="btn btn-primary quick-add-btn" onclick="app.quickAddBooking()" title="Quick add booking">+</button>
    
    <!-- Booking Modal -->
    <div class="modal" id="bookingModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modalTitle">Add Booking</h2>
            </div>
            <div class="modal-body">
                <div class="alert alert-success" id="successAlert"></div>
                <div class="alert alert-error" id="errorAlert"></div>
                
                <form id="bookingForm">
                    <div class="form-group">
                        <label for="bookingDate">Date</label>
                        <input type="date" id="bookingDate" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="clientName">Client Name</label>
                        <input type="text" id="clientName" required placeholder="Enter client name">
                    </div>
                    
                    <div class="form-group">
                        <label for="pricePerNight">Price per Night</label>
                        <input type="text" id="pricePerNight" placeholder="e.g., R500 or $50">
                    </div>
                    
                    <div class="form-group">
                        <label for="bookingNotes">Duties & Notes</label>
                        <textarea id="bookingNotes" placeholder="Pet care instructions, keys location, alarm codes, camera info, daily duties, etc."></textarea>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button class="btn btn-danger" id="deleteBtn" onclick="app.deleteBooking()" style="display:none; margin-right: auto;">Delete</button>
                <button class="btn btn-secondary" onclick="app.closeModal()">Cancel</button>
                <button class="btn btn-primary" onclick="app.saveBooking()">Save</button>
            </div>
        </div>
    </div>
    
    <script>
        // Main Application
        const app = {
            currentDate: new Date(),
            bookings: {},
            selectedDate: null,
            
            // Initialize the app
            async init() {
                await this.loadBookings();
                this.renderCalendar();
                this.updateStats();
                this.updateSidebar();
                this.setupEventListeners();
                this.loadThemePreferences();
            },
            
            // Load bookings from Python backend
            async loadBookings() {
                try {
                    const result = await pywebview.api.get_bookings();
                    this.bookings = JSON.parse(result);
                } catch (error) {
                    console.error('Error loading bookings:', error);
                }
            },
            
            // Setup event listeners
            setupEventListeners() {
                const searchInput = document.getElementById('searchInput');
                let searchTimeout;
                
                searchInput.addEventListener('input', (e) => {
                    clearTimeout(searchTimeout);
                    searchTimeout = setTimeout(() => {
                        this.searchBookings(e.target.value);
                    }, 300);
                });
                
                // Dark mode toggle
                const darkModeToggle = document.getElementById('darkModeToggle');
                darkModeToggle.addEventListener('change', (e) => {
                    this.toggleDarkMode(e.target.checked);
                });
                
                // Color picker
                const colorPicker = document.getElementById('colorPicker');
                colorPicker.addEventListener('input', (e) => {
                    this.changeThemeColor(e.target.value);
                });
            },
            
            // Load theme preferences from localStorage
            loadThemePreferences() {
                const darkMode = localStorage.getItem('darkMode') === 'true';
                const themeColor = localStorage.getItem('themeColor');
                
                if (darkMode) {
                    document.body.classList.add('dark-mode');
                    document.getElementById('darkModeToggle').checked = true;
                }
                
                if (themeColor) {
                    this.changeThemeColor(themeColor);
                    document.getElementById('colorPicker').value = themeColor;
                }
            },
            
            // Toggle dark mode
            toggleDarkMode(enabled) {
                if (enabled) {
                    document.body.classList.add('dark-mode');
                } else {
                    document.body.classList.remove('dark-mode');
                }
                localStorage.setItem('darkMode', enabled);
            },
            
            // Change theme color
            changeThemeColor(color) {
                const root = document.documentElement;
                root.style.setProperty('--bg-gradient-start', color);
                root.style.setProperty('--primary-color', color);
                
                // Calculate darker shade for gradient end
                const darker = this.adjustColor(color, -20);
                root.style.setProperty('--bg-gradient-end', darker);
                root.style.setProperty('--primary-hover', darker);
                
                localStorage.setItem('themeColor', color);
            },
            
            // Helper to adjust color brightness
            adjustColor(color, amount) {
                const num = parseInt(color.replace("#", ""), 16);
                const r = Math.max(0, Math.min(255, (num >> 16) + amount));
                const g = Math.max(0, Math.min(255, ((num >> 8) & 0x00FF) + amount));
                const b = Math.max(0, Math.min(255, (num & 0x0000FF) + amount));
                return "#" + (0x1000000 + r * 0x10000 + g * 0x100 + b).toString(16).slice(1);
            },
            
            // Search bookings
            async searchBookings(query) {
                if (!query.trim()) {
                    await this.loadBookings();
                    this.renderCalendar();
                    this.updateSidebar();
                    return;
                }
                
                try {
                    const result = await pywebview.api.search_bookings(query);
                    this.bookings = JSON.parse(result);
                    this.renderCalendar();
                    this.updateSidebar();
                } catch (error) {
                    console.error('Error searching bookings:', error);
                }
            },
            
            // Update sidebar with bookings list
            updateSidebar() {
                const bookingsList = document.getElementById('bookingsList');
                const bookingCount = document.getElementById('bookingCount');
                
                const sortedDates = Object.keys(this.bookings).sort();
                const count = sortedDates.length;
                
                bookingCount.textContent = count + ' booking' + (count !== 1 ? 's' : '') + ' scheduled';
                
                if (count === 0) {
                    bookingsList.innerHTML = '<div class="no-bookings">No bookings yet. Click a day on the calendar or use the + button to add one.</div>';
                    return;
                }
                
                bookingsList.innerHTML = '';
                
                sortedDates.forEach(date => {
                    const booking = this.bookings[date];
                    const bookingItem = document.createElement('div');
                    bookingItem.className = 'booking-item';
                    
                    const formattedDate = new Date(date + 'T00:00:00').toLocaleDateString('en-US', {
                        weekday: 'short',
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric'
                    });
                    
                    const summary = booking.notes ? booking.notes.substring(0, 50) + (booking.notes.length > 50 ? '...' : '') : 'No notes';
                    
                    let itemHTML = '<div class="booking-date">' + formattedDate + '</div>';
                    itemHTML += '<div class="booking-client">' + booking.client + '</div>';
                    if (booking.price) {
                        itemHTML += '<div class="booking-price">' + booking.price + ' per night</div>';
                    }
                    itemHTML += '<div class="booking-summary">' + summary + '</div>';
                    
                    bookingItem.innerHTML = itemHTML;
                    
                    bookingItem.addEventListener('click', () => {
                        this.openBookingModal(date, booking);
                    });
                    
                    bookingsList.appendChild(bookingItem);
                });
            },
            
            // Render the calendar
            renderCalendar() {
                const calendar = document.getElementById('calendar');
                calendar.innerHTML = '';
                
                const year = this.currentDate.getFullYear();
                const month = this.currentDate.getMonth();
                
                // Update header
                const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                                  'July', 'August', 'September', 'October', 'November', 'December'];
                document.getElementById('currentMonth').textContent = monthNames[month] + ' ' + year;
                
                // Add day headers
                const dayHeaders = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
                dayHeaders.forEach(day => {
                    const header = document.createElement('div');
                    header.className = 'day-header';
                    header.textContent = day;
                    calendar.appendChild(header);
                });
                
                // Get first day of month and number of days
                const firstDay = new Date(year, month, 1).getDay();
                const daysInMonth = new Date(year, month + 1, 0).getDate();
                const daysInPrevMonth = new Date(year, month, 0).getDate();
                
                // Add previous month's days
                for (let i = firstDay - 1; i >= 0; i--) {
                    const day = daysInPrevMonth - i;
                    this.createDayElement(day, month - 1, year, true);
                }
                
                // Add current month's days
                const today = new Date();
                for (let day = 1; day <= daysInMonth; day++) {
                    const isToday = day === today.getDate() && 
                                   month === today.getMonth() && 
                                   year === today.getFullYear();
                    this.createDayElement(day, month, year, false, isToday);
                }
                
                // Add next month's days
                const totalCells = calendar.children.length - 7;
                const remainingCells = 42 - totalCells - 7;
                for (let day = 1; day <= remainingCells; day++) {
                    this.createDayElement(day, month + 1, year, true);
                }
            },
            
            // Create a day element
            createDayElement(day, month, year, otherMonth, isToday) {
                otherMonth = otherMonth || false;
                isToday = isToday || false;
                
                const calendar = document.getElementById('calendar');
                const dayEl = document.createElement('div');
                dayEl.className = 'day';
                
                if (otherMonth) dayEl.classList.add('other-month');
                if (isToday) dayEl.classList.add('today');
                
                // Format date as YYYY-MM-DD
                const dateStr = year + '-' + String(month + 1).padStart(2, '0') + '-' + String(day).padStart(2, '0');
                
                // Check if this day has a booking
                const booking = this.bookings[dateStr];
                
                if (booking) {
                    dayEl.classList.add('booked');
                    dayEl.innerHTML = '<div class="day-number">' + day + '</div><div class="day-client">' + booking.client + '</div>';
                } else {
                    dayEl.innerHTML = '<div class="day-number">' + day + '</div>';
                }
                
                dayEl.addEventListener('click', () => this.openBookingModal(dateStr, booking));
                calendar.appendChild(dayEl);
            },
            
            // Quick add booking
            quickAddBooking() {
                const today = new Date();
                const dateStr = today.toISOString().split('T')[0];
                this.openBookingModal(dateStr, null, false);
            },
            
            // Open booking modal
            openBookingModal(date, booking, readonly) {
                booking = booking || null;
                readonly = readonly === undefined ? true : readonly;
                
                this.selectedDate = date;
                const modal = document.getElementById('bookingModal');
                const title = document.getElementById('modalTitle');
                const dateInput = document.getElementById('bookingDate');
                const clientInput = document.getElementById('clientName');
                const notesInput = document.getElementById('bookingNotes');
                const priceInput = document.getElementById('pricePerNight');
                const deleteBtn = document.getElementById('deleteBtn');
                
                dateInput.value = date;
                dateInput.readOnly = readonly && booking !== null;
                
                if (booking) {
                    title.textContent = 'Edit Booking';
                    clientInput.value = booking.client;
                    notesInput.value = booking.notes;
                    priceInput.value = booking.price || '';
                    deleteBtn.style.display = 'block';
                } else {
                    title.textContent = 'Add Booking';
                    clientInput.value = '';
                    notesInput.value = '';
                    priceInput.value = '';
                    deleteBtn.style.display = 'none';
                }
                
                modal.classList.add('active');
            },
            
            // Close modal
            closeModal() {
                const modal = document.getElementById('bookingModal');
                modal.classList.remove('active');
                this.hideAlerts();
                
                // Reset date input readonly state
                document.getElementById('bookingDate').readOnly = false;
            },
            
            // Save booking
            async saveBooking() {
                const date = document.getElementById('bookingDate').value;
                const client = document.getElementById('clientName').value.trim();
                const notes = document.getElementById('bookingNotes').value.trim();
                const price = document.getElementById('pricePerNight').value.trim();
                
                if (!client) {
                    this.showError('Please enter a client name');
                    return;
                }
                
                if (!date) {
                    this.showError('Please select a date');
                    return;
                }
                
                try {
                    const existingBooking = this.bookings[date];
                    let result;
                    
                    if (existingBooking) {
                        result = await pywebview.api.update_booking(date, client, notes, price);
                    } else {
                        result = await pywebview.api.add_booking(date, client, notes, price);
                    }
                    
                    const data = JSON.parse(result);
                    
                    if (data.success) {
                        this.showSuccess('Booking saved successfully!');
                        await this.loadBookings();
                        this.renderCalendar();
                        this.updateStats();
                        this.updateSidebar();
                        
                        setTimeout(() => this.closeModal(), 1500);
                    } else {
                        this.showError('Error saving booking');
                    }
                } catch (error) {
                    console.error('Error saving booking:', error);
                    this.showError('Error saving booking');
                }
            },
            
            // Delete booking
            async deleteBooking() {
                if (!confirm('Are you sure you want to delete this booking?')) {
                    return;
                }
                
                try {
                    const date = this.selectedDate;
                    const result = await pywebview.api.delete_booking(date);
                    const data = JSON.parse(result);
                    
                    if (data.success) {
                        this.showSuccess('Booking deleted successfully!');
                        await this.loadBookings();
                        this.renderCalendar();
                        this.updateStats();
                        this.updateSidebar();
                        
                        setTimeout(() => this.closeModal(), 1500);
                    } else {
                        this.showError('Error deleting booking');
                    }
                } catch (error) {
                    console.error('Error deleting booking:', error);
                    this.showError('Error deleting booking');
                }
            },
            
            // Export to CSV
            async exportCSV() {
                try {
                    const result = await pywebview.api.export_csv();
                    const data = JSON.parse(result);
                    
                    if (data.success) {
                        alert('Bookings exported successfully to:\n' + data.filepath);
                    } else {
                        alert('Error exporting bookings');
                    }
                } catch (error) {
                    console.error('Error exporting:', error);
                    alert('Error exporting bookings');
                }
            },
            
            // Navigation
            prevMonth() {
                this.currentDate.setMonth(this.currentDate.getMonth() - 1);
                this.renderCalendar();
                this.updateStats();
            },
            
            nextMonth() {
                this.currentDate.setMonth(this.currentDate.getMonth() + 1);
                this.renderCalendar();
                this.updateStats();
            },
            
            showToday() {
                this.currentDate = new Date();
                this.renderCalendar();
                this.updateStats();
            },
            
            // Update statistics
            updateStats() {
                const total = Object.keys(this.bookings).length;
                const currentMonth = this.currentDate.getMonth();
                const currentYear = this.currentDate.getFullYear();
                
                let thisMonth = 0;
                for (const date in this.bookings) {
                    const bookingDate = new Date(date + 'T00:00:00');
                    if (bookingDate.getMonth() === currentMonth && 
                        bookingDate.getFullYear() === currentYear) {
                        thisMonth++;
                    }
                }
                
                document.getElementById('totalBookings').textContent = total;
                document.getElementById('thisMonthBookings').textContent = thisMonth;
            },
            
            // Alert helpers
            showSuccess(message) {
                const alert = document.getElementById('successAlert');
                alert.textContent = message;
                alert.classList.add('show');
                this.hideError();
            },
            
            showError(message) {
                const alert = document.getElementById('errorAlert');
                alert.textContent = message;
                alert.classList.add('show');
                this.hideSuccess();
            },
            
            hideSuccess() {
                const alert = document.getElementById('successAlert');
                alert.classList.remove('show');
            },
            
            hideError() {
                const alert = document.getElementById('errorAlert');
                alert.classList.remove('show');
            },
            
            hideAlerts() {
                this.hideSuccess();
                this.hideError();
            }
        };
        
        // Initialize app when ready
        window.addEventListener('pywebviewready', () => {
            app.init();
        });
    </script>
</body>
</html>
"""


def main():
    """Main entry point for the application"""
    # Create API instance
    api = API()
    
    # Create window
    window = webview.create_window(
        'Housesitting Scheduler',
        html=HTML_CONTENT,
        js_api=api,
        width=1400,
        height=900,
        resizable=True
    )
    
    # Start the application
    webview.start(debug=False)


if __name__ == '__main__':
    main()