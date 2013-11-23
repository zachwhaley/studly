package com.studly.model;

import java.util.ArrayList;


public class StudlyGroup {

    private String name;
    private boolean joined;

    public String getName() {
        return this.name;
    }

    public boolean isJoined() {
        return this.joined;
    }

    public static class List extends ArrayList<StudlyGroup> {
    }

}
