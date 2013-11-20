package com.studly.network;

import java.util.Arrays;

import com.octo.android.robospice.request.retrofit.RetrofitSpiceRequest;
import com.studly.model.StudlyEvent;

public class RequestStudlyEvents extends RetrofitSpiceRequest<StudlyEvent.List, StudlyApi> {

	static final StudlyEvent[] EVENTS = { 
		new StudlyEvent("Foo"),
		new StudlyEvent("Bar") 
	};

	public RequestStudlyEvents() {
		super(StudlyEvent.List.class, StudlyApi.class);
	}

	@Override
	public StudlyEvent.List loadDataFromNetwork() throws Exception {
		StudlyEvent.List events = new StudlyEvent.List();
		events.addAll(Arrays.asList(EVENTS));
		return events;
	}

}
