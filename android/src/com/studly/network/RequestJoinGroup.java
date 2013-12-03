package com.studly.network;

import com.octo.android.robospice.request.retrofit.RetrofitSpiceRequest;
import com.studly.model.StudlyMapping;

public class RequestJoinGroup extends RetrofitSpiceRequest<StudlyMapping, StudlyApi> {

    private StudlyMapping mMapping;
    private String mEmail;

    public RequestJoinGroup(StudlyMapping mapping, String email) {
        super(StudlyMapping.class, StudlyApi.class);
        mMapping = mapping;
        mEmail = email;
    }

    @Override
    public StudlyMapping loadDataFromNetwork() throws Exception {
        return getService().joinGroup(mMapping.getTitle(), mMapping.getCalendarId(), mEmail);
    }

}
