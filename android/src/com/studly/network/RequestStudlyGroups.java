package com.studly.network;

import com.octo.android.robospice.request.retrofit.RetrofitSpiceRequest;
import com.studly.model.StudlyGroup;

public class RequestStudlyGroups extends RetrofitSpiceRequest<StudlyGroup.List, StudlyApi> {

    public RequestStudlyGroups() {
        super(StudlyGroup.List.class, StudlyApi.class);
    }

    @Override
    public StudlyGroup.List loadDataFromNetwork() throws Exception {
        return getService().getGroups();
    }

}
