package com.studly.model;

import java.util.ArrayList;


public class StudlyMapping {

    private String title;
    private String htmlLink;
    private ArrayList<String> reflectorList;
    private String calendarId;
    private String nextStartTime;
    private String recurringStartTime;
    private String location;
    private double latitude;
    private double longitude;

    public static class List extends ArrayList<StudlyMapping> {
    }

    public String getTitle() {
        return title;
    }

    public String getHtmlLink() {
        return htmlLink;
    }

    public ArrayList<String> getReflectorList() {
        return reflectorList;
    }

    public String getCalendarId() {
        return calendarId;
    }

    public String getNextStartTime() {
        return nextStartTime;
    }

    public String getRecurringStartTime() {
        return recurringStartTime;
    }

    public String getLocation() {
        return location;
    }

    public double getLatitude() {
        return latitude;
    }

    public double getLongitude() {
        return longitude;
    }


}
