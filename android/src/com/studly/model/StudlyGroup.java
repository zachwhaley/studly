package com.studly.model;

import java.util.ArrayList;


public class StudlyGroup {

    private String name;
    private String joined;

    public String getName() {
        return name;
    }

    public boolean isJoined() {
        return Boolean.getBoolean(joined);
    }

    public static class List extends ArrayList<StudlyGroup> {
    }

}
