package com.studly.model;

import java.util.ArrayList;


public class StudlyEvent {
	
	private String mName;
	
	public StudlyEvent(String name) {
		mName = name;
	}
	
	public String getName() {
		return mName;
	}

	public static class List extends ArrayList<StudlyEvent> {
	}
}
