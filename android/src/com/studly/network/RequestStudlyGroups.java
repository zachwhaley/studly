package com.studly.network;

import com.octo.android.robospice.request.retrofit.RetrofitSpiceRequest;
import com.studly.model.StudlyMapping;

public class RequestStudlyGroups extends RetrofitSpiceRequest<StudlyMapping.List, StudlyApi> {

    public RequestStudlyGroups() {
        super(StudlyMapping.List.class, StudlyApi.class);
    }

    @Override
    public StudlyMapping.List loadDataFromNetwork() throws Exception {
        return getService().getMappings();
    }

}
