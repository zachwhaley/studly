package com.studly.model;

import java.util.ArrayList;


public class StudlyEvent {
	
	private String mName;
	private boolean mJoined;
	
	public StudlyEvent(String name) {
		mName = name;
	}
	
	public String getName() {
		return mName;
	}

    public boolean isJoined() {
        return mJoined;
    }
    
	public static class List extends ArrayList<StudlyEvent> {
	}

}
